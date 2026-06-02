export enum SpeakerRole {
  BUYER = '买方',
  SELLER = '卖方',
  ANALYST = '分析师',
  UNKNOWN = '未知',
}

export interface TranscriptSegment {
  start_time: number;
  end_time: number;
  speaker: string;
  speaker_role: SpeakerRole;
  text: string;
}

export interface TradingStrategy {
  strategy_summary: string;
  entry_points: string[];
  exit_points: string[];
  position_sizing: string;
  risk_management: string;
  time_horizon: string;
  confidence_level: number;
}

export interface MeetingResponse {
  meeting_id: string;
  timestamp: string;
  transcript_segments: TranscriptSegment[];
  policy_analysis: string;
  supply_demand_analysis: string;
  buyer_viewpoints: string[];
  seller_viewpoints: string[];
  trading_strategy: TradingStrategy;
  markdown_report: string;
}

export interface CarbonPriceData {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface EmissionData {
  year: number;
  baseline: number;
  target: number;
  actual: number;
  reduction_rate: number;
}

export interface EmailRequest {
  recipients: string[];
  subject: string;
  markdown_content: string;
}
