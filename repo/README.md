# 碳交易市场策略会系统

全栈应用，用于处理碳交易市场策略会议，包含语音转写、说话人分离、AI分析和交易策略生成。

## 系统架构

### 后端 (FastAPI)
- **语音转写**: Whisper
- **说话人分离**: pyannote.audio
- **AI分析**: OpenAI GPT-4
- **邮件发送**: SMTP

### 前端 (React + TypeScript)
- **UI框架**: Ant Design
- **图表**: ECharts
- **构建工具**: Vite

## 功能特性

1. **会议音频处理**
   - 上传会议录音（支持WAV、MP3、M4A、FLAC）
   - Whisper自动语音转写
   - pyannote区分买卖方和分析师
   - 角色自动识别（买方/卖方/分析师）

2. **AI智能分析**
   - 政策分析提取
   - 供需格局研判
   - 买卖双方观点总结
   - 交易策略生成
   - Markdown报告自动生成

3. **市场数据展示**
   - 碳价K线图
   - 减排曲线图

4. **报告分发**
   - Markdown格式会议纪要
   - 邮件发送给投资决策委员会

## 快速开始

### 环境配置

1. 复制环境变量文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入必要的API密钥：
```
OPENAI_API_KEY=your_openai_api_key
PYANNOTE_AUTH_TOKEN=your_pyannote_auth_token
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_email@example.com
SMTP_PASSWORD=your_email_password
```

### 后端启动

```bash
cd backend
pip install -r ../requirements.txt
python main.py
```

后端服务将在 `http://localhost:8000` 启动。

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:3000` 启动。

## API接口

### POST /api/meeting/process
上传并处理会议音频文件

### GET /api/market/carbon-price
获取碳价K线数据

### GET /api/market/emission-curve
获取减排曲线数据

### POST /api/email/send
发送Markdown邮件

## 项目结构

```
.
├── backend/
│   ├── main.py                 # FastAPI主程序
│   ├── api/
│   │   └── routes.py           # API路由
│   ├── models/
│   │   └── schemas.py          # 数据模型
│   └── services/
│       ├── whisper_service.py  # Whisper语音转写
│       ├── pyannote_service.py # 说话人分离
│       ├── openai_service.py   # OpenAI分析
│       └── email_service.py    # 邮件服务
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CarbonPriceChart.tsx    # K线图组件
│   │   │   ├── EmissionCurveChart.tsx  # 减排曲线组件
│   │   │   ├── MeetingMinutes.tsx      # 会议纪要组件
│   │   │   └── StrategyPanel.tsx       # 策略面板组件
│   │   ├── services/
│   │   │   └── api.ts                  # API调用
│   │   ├── types/
│   │   │   └── index.ts                # 类型定义
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── index.html
│   ├── vite.config.ts
│   └── package.json
├── requirements.txt
├── package.json
└── .env.example
```

## 注意事项

- 首次运行时，Whisper和pyannote模型会自动下载，需要较长时间
- 确保有足够的磁盘空间存储模型文件
- 建议使用GPU加速语音处理
- 系统包含Mock模式，无API密钥时也能正常运行演示
