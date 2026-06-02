import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import aiofiles
import tempfile
import logging
from datetime import datetime

from api.routes import router as api_router
from services.whisper_service import WhisperService
from services.pyannote_service import PyannoteService
from services.openai_service import OpenAIService
from services.email_service import EmailService
from models.schemas import (
    MeetingResponse,
    TranscriptSegment,
    TradingStrategy,
    EmailRequest
)

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="碳交易市场策略会系统", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

whisper_service = WhisperService()
pyannote_service = PyannoteService()
openai_service = OpenAIService()
email_service = EmailService()


@app.post("/api/meeting/process", response_model=MeetingResponse)
async def process_meeting(audio_file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            async with aiofiles.open(tmp.name, 'wb') as f:
                content = await audio_file.read()
                await f.write(content)
            temp_path = tmp.name

        logger.info("开始说话人分离...")
        speaker_segments = pyannote_service.diarize(temp_path)
        logger.info(f"识别到 {len(speaker_segments)} 个说话人片段")

        logger.info("开始语音转写...")
        transcript_segments = whisper_service.transcribe_with_speakers(
            temp_path, speaker_segments
        )

        full_transcript = "\n".join([
            f"[{seg.speaker}] {seg.text}"
            for seg in transcript_segments
        ])

        logger.info("开始AI分析和策略生成...")
        analysis = openai_service.analyze_meeting(full_transcript)
        strategy = openai_service.generate_trading_strategy(analysis)
        markdown_content = openai_service.generate_markdown_report(
            transcript_segments, analysis, strategy
        )

        os.unlink(temp_path)

        return MeetingResponse(
            meeting_id=datetime.now().strftime("%Y%m%d-%H%M%S"),
            timestamp=datetime.now(),
            transcript_segments=transcript_segments,
            policy_analysis=analysis["policy_analysis"],
            supply_demand_analysis=analysis["supply_demand_analysis"],
            buyer_viewpoints=analysis["buyer_viewpoints"],
            seller_viewpoints=analysis["seller_viewpoints"],
            trading_strategy=strategy,
            markdown_report=markdown_content
        )

    except Exception as e:
        logger.error(f"处理会议失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/email/send")
async def send_email(request: EmailRequest):
    try:
        success = email_service.send_markdown_email(
            recipients=request.recipients,
            subject=request.subject,
            markdown_content=request.markdown_content
        )
        return {"success": success, "message": "邮件发送成功" if success else "邮件发送失败"}
    except Exception as e:
        logger.error(f"发送邮件失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market/carbon-price")
async def get_carbon_price_data():
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta

    date_range = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    base_price = 70
    prices = base_price + np.cumsum(np.random.randn(len(date_range)) * 2)
    prices = np.clip(prices, 40, 120)

    kline_data = []
    for i, date in enumerate(date_range):
        open_p = prices[i]
        close_p = prices[i] + np.random.randn() * 1.5
        high_p = max(open_p, close_p) + abs(np.random.randn())
        low_p = min(open_p, close_p) - abs(np.random.randn())
        volume = int(100000 + np.random.randint(50000, 200000))
        kline_data.append({
            "date": date.strftime('%Y-%m-%d'),
            "open": round(open_p, 2),
            "close": round(close_p, 2),
            "high": round(high_p, 2),
            "low": round(low_p, 2),
            "volume": volume
        })

    return {"data": kline_data}


@app.get("/api/market/emission-curve")
async def get_emission_curve_data():
    import numpy as np

    years = list(range(2020, 2031))
    baseline_emissions = [100, 105, 102, 98, 95, 90, 85, 80, 75, 70, 65]
    target_emissions = [100, 103, 100, 95, 90, 85, 80, 75, 70, 65, 60]
    actual_emissions = [100, 106, 104, 101, 97, 92, 87, 82, 77, 72, 67]
    reduction_rate = [
        round((baseline_emissions[i] - actual_emissions[i]) / baseline_emissions[i] * 100, 2)
        for i in range(len(years))
    ]

    return {
        "data": [
            {
                "year": years[i],
                "baseline": baseline_emissions[i],
                "target": target_emissions[i],
                "actual": actual_emissions[i],
                "reduction_rate": reduction_rate[i]
            }
            for i in range(len(years))
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
