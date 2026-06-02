import os
import json
import logging
from typing import List, Dict, Any
from datetime import datetime

from openai import OpenAI
from models.schemas import TranscriptSegment, TradingStrategy

logger = logging.getLogger(__name__)


class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self._client = None
        logger.info("OpenAIService initialized")

    def _get_client(self):
        if self._client is None:
            if self.api_key:
                self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            else:
                logger.warning("OpenAI API key not provided. Using mock mode.")
                self._client = None
        return self._client

    def analyze_meeting(self, transcript: str) -> Dict[str, Any]:
        client = self._get_client()

        if client is None:
            return self._mock_analyze_meeting()

        system_prompt = """
你是一位资深的碳交易市场分析师，擅长从会议讨论中提取关键信息。
请分析以下碳交易策略会的讨论内容，提取：
1. 政策分析：涉及的政策法规、监管动态、减排目标等
2. 供需分析：市场供需格局、配额缺口/富余、行业影响等
3. 买方观点：买方代表的核心诉求、预期价位、操作建议等
4. 卖方观点：卖方代表的核心诉求、预期价位、操作建议等

请以JSON格式输出，包含以下字段：
- policy_analysis: string
- supply_demand_analysis: string
- buyer_viewpoints: string[]
- seller_viewpoints: string[]
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript}
            ],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result

    def generate_trading_strategy(self, analysis: Dict[str, Any]) -> TradingStrategy:
        client = self._get_client()

        if client is None:
            return self._mock_generate_trading_strategy()

        system_prompt = """
你是一位资深的碳交易策略师，基于市场分析生成具体的交易策略。
请根据以下分析结果，生成可执行的交易策略，以JSON格式输出，包含：
- strategy_summary: 策略概述
- entry_points: 入场点位建议（数组）
- exit_points: 出场点位建议（数组）
- position_sizing: 仓位管理建议
- risk_management: 风险管理措施
- time_horizon: 操作时间周期
- confidence_level: 策略置信度（0-1之间的浮点数）
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(analysis, ensure_ascii=False)}
            ],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return TradingStrategy(**result)

    def generate_markdown_report(
        self,
        transcript_segments: List[TranscriptSegment],
        analysis: Dict[str, Any],
        strategy: TradingStrategy
    ) -> str:
        client = self._get_client()

        if client is None:
            return self._mock_generate_markdown_report(
                transcript_segments, analysis, strategy
            )

        system_prompt = """
你是一位专业的金融报告撰写人，请将碳交易策略会的讨论内容、分析和交易策略整理成一份专业的Markdown格式会议纪要。

报告应包含以下部分：
1. 会议概要（时间、参与方、主题）
2. 会议讨论纪要（按说话人分类展示）
3. 政策分析
4. 供需分析
5. 买卖双方博弈观点
6. 交易策略建议
7. 执行建议与风险提示

请使用专业的金融报告风格，确保内容清晰、重点突出。
"""

        context = {
            "transcript_segments": [seg.model_dump() for seg in transcript_segments],
            "analysis": analysis,
            "strategy": strategy.model_dump()
        }

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(context, ensure_ascii=False)}
            ]
        )

        return response.choices[0].message.content

    def _mock_analyze_meeting(self) -> Dict[str, Any]:
        return {
            "policy_analysis": "国家发改委预计将在2025年收紧碳配额总量约5%，同时可能将建材、有色等高耗能行业纳入全国碳市场。欧盟CBAM机制将对出口企业造成一定压力，但长期来看将推动国内碳价与国际接轨。",
            "supply_demand_analysis": "当前全国碳市场配额供需比约为1.02:1，略微供过于求。短期来看，电力行业旺季将增加碳排放需求；长期来看，新行业纳入将大幅增加配额需求，预计2025年供需缺口将扩大至8-10%。",
            "buyer_viewpoints": [
                "下半年电力行业进入旺季，碳排放将显著增加",
                "建议在70-75元/吨区间逐步建仓，锁定成本",
                "新行业纳入预期将推动碳价长期上涨",
                "当前价位相对于未来预期仍处于低位"
            ],
            "seller_viewpoints": [
                "通过技术改造实现超额减排，有30万吨富余配额可售",
                "担心政策收紧预期已被市场消化，存在回调风险",
                "建议逢高卖出，在价格回调后再回补",
                "CBAM可能导致部分高耗能企业减产，短期需求承压"
            ]
        }

    def _mock_generate_trading_strategy(self) -> TradingStrategy:
        return TradingStrategy(
            strategy_summary="区间震荡偏多策略。在政策收紧预期和新行业纳入的背景下，碳价中长期看涨，但短期需警惕回调风险。建议采取低买高卖的区间操作策略，同时保留部分仓位等待突破。",
            entry_points=[
                "价格回调至65-70元/吨区间，分批建仓30%",
                "价格突破85元/吨阻力位，追涨加仓20%",
                "价格回踩60元/吨支撑位，加倍建仓40%"
            ],
            exit_points=[
                "价格上涨至80-85元/吨区间，止盈50%仓位",
                "价格跌破60元/吨支撑位，止损离场",
                "价格在75-80元区间震荡超过2周，减仓30%"
            ],
            position_sizing="总仓位控制在资金的15-20%，单笔交易风险不超过总资金的2%。建仓采用分批进场方式，首次建仓30%，确认趋势后再加仓。",
            risk_management="设置60元/吨作为关键止损位，跌破则止损离场。密切关注政策发布时间窗口，政策落地前可适当降低仓位。使用期权对冲尾部风险。",
            time_horizon="主要操作周期为1-3个月的中线交易，同时保留10%仓位作为长期配置（6-12个月）。",
            confidence_level=0.78
        )

    def _mock_generate_markdown_report(
        self,
        transcript_segments: List[TranscriptSegment],
        analysis: Dict[str, Any],
        strategy: TradingStrategy
    ) -> str:
        from datetime import datetime

        report = f"""# 碳交易市场策略会会议纪要

**会议时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
**会议主题**: 2024年Q4碳交易市场展望与策略研讨
**参与方**: 分析师团队、买方交易员、卖方交易员

---

## 一、会议讨论纪要

### 参会人员观点汇总

| 角色 | 发言要点 |
|------|----------|
| **分析师** | 政策面分析、供需格局解读、市场趋势判断 |
| **买方** | 配额缺口情况、需求展望、买入策略建议 |
| **卖方** | 减排成果、富余配额处置、卖出策略建议 |

---

## 二、政策分析

{analysis['policy_analysis']}

---

## 三、供需分析

{analysis['supply_demand_analysis']}

---

## 四、买卖双方博弈观点

### 买方观点
{chr(10).join([f"- {v}" for v in analysis['buyer_viewpoints']])}

### 卖方观点
{chr(10).join([f"- {v}" for v in analysis['seller_viewpoints']])}

---

## 五、交易策略建议

### 策略概述
{strategy.strategy_summary}

### 入场点位
{chr(10).join([f"- {ep}" for ep in strategy.entry_points])}

### 出场点位
{chr(10).join([f"- {ep}" for ep in strategy.exit_points])}

### 仓位管理
{strategy.position_sizing}

### 风险管理
{strategy.risk_management}

### 操作周期
{strategy.time_horizon}

### 策略置信度
{strategy.confidence_level * 100:.1f}%

---

## 六、执行建议与风险提示

### 立即执行
1. 在65-70元/吨区间建立初始观察仓位
2. 设置60元/吨止损预警
3. 密切关注发改委政策发布时间窗口

### 待确认信号
1. 新行业纳入政策正式公布
2. 碳价有效突破85元/吨阻力位
3. 成交量放大确认趋势

### 风险提示
- **政策风险**: 政策落地时间或力度不及预期
- **市场风险**: 宏观经济下行导致碳排放需求下降
- **流动性风险**: 碳市场流动性不足导致滑点过大

---

**发送至**: 投资决策委员会
**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        return report
