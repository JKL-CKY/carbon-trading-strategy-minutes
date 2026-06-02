import os
import logging
from typing import List, Dict, Any
from models.schemas import TranscriptSegment, SpeakerRole

logger = logging.getLogger(__name__)


class WhisperService:
    def __init__(self):
        self.model_name = os.getenv("WHISPER_MODEL", "base")
        self._model = None
        logger.info(f"WhisperService initialized with model: {self.model_name}")

    def _load_model(self):
        if self._model is None:
            try:
                import whisper
                self._model = whisper.load_model(self.model_name)
                logger.info("Whisper model loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load Whisper model: {e}. Using mock mode.")
                self._model = None
        return self._model

    def transcribe_with_speakers(
        self,
        audio_path: str,
        speaker_segments: List[Dict[str, Any]]
    ) -> List[TranscriptSegment]:
        model = self._load_model()

        if model is None:
            return self._mock_transcribe_with_speakers(audio_path, speaker_segments)

        result = model.transcribe(audio_path, word_timestamps=True)
        segments = result["segments"]

        transcript_segments = []
        for seg in segments:
            start = seg["start"]
            end = seg["end"]
            text = seg["text"].strip()

            speaker = self._assign_speaker(start, end, speaker_segments)
            speaker_role = self._classify_speaker_role(text, speaker)

            transcript_segments.append(TranscriptSegment(
                start_time=start,
                end_time=end,
                speaker=speaker,
                speaker_role=speaker_role,
                text=text
            ))

        return transcript_segments

    def _assign_speaker(
        self,
        start: float,
        end: float,
        speaker_segments: List[Dict[str, Any]]
    ) -> str:
        mid_point = (start + end) / 2
        for seg in speaker_segments:
            if seg["start"] <= mid_point <= seg["end"]:
                return seg["speaker"]
        return "SPEAKER_UNKNOWN"

    def _classify_speaker_role(self, text: str, speaker: str) -> SpeakerRole:
        text_lower = text.lower()

        buyer_keywords = [
            "买入", "做多", "看涨", "需求", "需要配额", "排放超标",
            "buy", "long", "demand", "need", "shortage"
        ]

        seller_keywords = [
            "卖出", "做空", "看跌", "供应", "配额富余", "减排超额",
            "sell", "short", "supply", "surplus", "excess"
        ]

        analyst_keywords = [
            "分析", "预测", "趋势", "政策", "宏观", "数据",
            "analyze", "forecast", "trend", "policy", "macro", "data"
        ]

        buyer_score = sum(1 for kw in buyer_keywords if kw in text_lower)
        seller_score = sum(1 for kw in seller_keywords if kw in text_lower)
        analyst_score = sum(1 for kw in analyst_keywords if kw in text_lower)

        max_score = max(buyer_score, seller_score, analyst_score)

        if max_score == 0:
            return SpeakerRole.UNKNOWN
        elif buyer_score == max_score:
            return SpeakerRole.BUYER
        elif seller_score == max_score:
            return SpeakerRole.SELLER
        else:
            return SpeakerRole.ANALYST

    def _mock_transcribe_with_speakers(
        self,
        audio_path: str,
        speaker_segments: List[Dict[str, Any]]
    ) -> List[TranscriptSegment]:
        mock_transcripts = [
            {
                "start": 0.0,
                "end": 15.5,
                "speaker": "SPEAKER_00",
                "role": SpeakerRole.ANALYST,
                "text": "各位好，今天我们讨论碳交易市场的最新动态。从政策面来看，国家发改委近期可能出台新的减排目标，预计2025年碳配额总量将收紧5%左右。"
            },
            {
                "start": 15.5,
                "end": 32.0,
                "speaker": "SPEAKER_01",
                "role": SpeakerRole.BUYER,
                "text": "我们公司今年的排放量预计会超标15%，需要在市场上买入约20万吨配额。从需求端看，下半年电力行业进入旺季，碳排放肯定会增加，我认为碳价会持续上涨。"
            },
            {
                "start": 32.0,
                "end": 48.5,
                "speaker": "SPEAKER_02",
                "role": SpeakerRole.SELLER,
                "text": "我们这边通过技术改造，今年减排效果很好，预计有30万吨富余配额可以出售。不过我担心政策收紧可能是预期已经消化了，现在碳价处于高位，是不是应该逢高卖出？"
            },
            {
                "start": 48.5,
                "end": 65.0,
                "speaker": "SPEAKER_00",
                "role": SpeakerRole.ANALYST,
                "text": "从供需基本面分析，目前全国碳市场的配额供需比大约是1.02:1，略微供过于求。但是考虑到明年可能纳入更多行业，如建材、有色等，长期需求会大幅增加。"
            },
            {
                "start": 65.0,
                "end": 82.0,
                "speaker": "SPEAKER_01",
                "role": SpeakerRole.BUYER,
                "text": "没错，建材行业每年的碳排放量约30亿吨，如果纳入的话，配额需求会激增。我们建议在当前70-75元/吨的价位逐步建仓，锁定成本。"
            },
            {
                "start": 82.0,
                "end": 98.0,
                "speaker": "SPEAKER_02",
                "role": SpeakerRole.SELLER,
                "text": "但短期来看，欧盟碳边境调节机制CBAM可能会对出口企业造成压力，部分高耗能企业可能会减产，这会减少配额需求。我觉得可以先卖出一部分，等回调再买回来。"
            },
            {
                "start": 98.0,
                "end": 115.0,
                "speaker": "SPEAKER_00",
                "role": SpeakerRole.ANALYST,
                "text": "综合各方观点，我建议采取区间操作策略。支撑位在65元，阻力位在85元。可以在65-70元区间买入，80-85元区间卖出，止损位设在60元。"
            }
        ]

        return [
            TranscriptSegment(
                start_time=item["start"],
                end_time=item["end"],
                speaker=item["speaker"],
                speaker_role=item["role"],
                text=item["text"]
            )
            for item in mock_transcripts
        ]
