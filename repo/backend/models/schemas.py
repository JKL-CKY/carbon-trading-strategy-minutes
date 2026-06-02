from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class SpeakerRole(str, Enum):
    BUYER = "买方"
    SELLER = "卖方"
    ANALYST = "分析师"
    UNKNOWN = "未知"


class TranscriptSegment(BaseModel):
    start_time: float
    end_time: float
    speaker: str
    speaker_role: SpeakerRole
    text: str


class TradingStrategy(BaseModel):
    strategy_summary: str
    entry_points: List[str]
    exit_points: List[str]
    position_sizing: str
    risk_management: str
    time_horizon: str
    confidence_level: float


class MeetingResponse(BaseModel):
    meeting_id: str
    timestamp: datetime
    transcript_segments: List[TranscriptSegment]
    policy_analysis: str
    supply_demand_analysis: str
    buyer_viewpoints: List[str]
    seller_viewpoints: List[str]
    trading_strategy: TradingStrategy
    markdown_report: str


class EmailRequest(BaseModel):
    recipients: List[str]
    subject: str
    markdown_content: str


class CarbonPriceData(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class EmissionData(BaseModel):
    year: int
    baseline: float
    target: float
    actual: float
    reduction_rate: float
