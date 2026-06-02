import React, { useState, useEffect } from 'react';
import { Layout, Menu, Typography, Row, Col, Card, Button, Upload, message, Progress } from 'antd';
import {
  DashboardOutlined,
  LineChartOutlined,
  BarChartOutlined,
  FileTextOutlined,
  MailOutlined,
  UploadOutlined,
} from '@ant-design/icons';
import type { UploadProps } from 'antd';
import CarbonPriceChart from './components/CarbonPriceChart';
import EmissionCurveChart from './components/EmissionCurveChart';
import MeetingMinutes from './components/MeetingMinutes';
import StrategyPanel from './components/StrategyPanel';
import { meetingApi } from './services/api';
import type { MeetingResponse, CarbonPriceData, EmissionData } from './types';

const { Header, Sider, Content } = Layout;
const { Title } = Typography;

const App: React.FC = () => {
  const [activeKey, setActiveKey] = useState('dashboard');
  const [loading, setLoading] = useState(false);
  const [meetingData, setMeetingData] = useState<MeetingResponse | null>(null);
  const [carbonPriceData, setCarbonPriceData] = useState<CarbonPriceData[]>([]);
  const [emissionData, setEmissionData] = useState<EmissionData[]>([]);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    loadMarketData();
  }, []);

  const loadMarketData = async () => {
    try {
      const [priceData, emission] = await Promise.all([
        meetingApi.getCarbonPrice(),
        meetingApi.getEmissionCurve(),
      ]);
      setCarbonPriceData(priceData);
      setEmissionData(emission);
    } catch (error) {
      message.error('加载市场数据失败');
    }
  };

  const uploadProps: UploadProps = {
    name: 'audio_file',
    accept: '.wav,.mp3,.m4a,.flac',
    showUploadList: false,
    beforeUpload: async (file) => {
      setLoading(true);
      setProgress(0);

      const interval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 10, 90));
      }, 500);

      try {
        const result = await meetingApi.processMeeting(file);
        setMeetingData(result);
        setActiveKey('meeting');
        message.success('会议处理完成');
      } catch (error) {
        message.error('处理会议音频失败');
      } finally {
        clearInterval(interval);
        setProgress(100);
        setLoading(false);
        setTimeout(() => setProgress(0), 1000);
      }

      return false;
    },
  };

  const menuItems = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: '市场概览',
    },
    {
      key: 'price',
      icon: <LineChartOutlined />,
      label: '碳价走势',
    },
    {
      key: 'emission',
      icon: <BarChartOutlined />,
      label: '减排曲线',
    },
    {
      key: 'meeting',
      icon: <FileTextOutlined />,
      label: '会议纪要',
      disabled: !meetingData,
    },
    {
      key: 'strategy',
      icon: <LineChartOutlined />,
      label: '交易策略',
      disabled: !meetingData,
    },
  ];

  const renderContent = () => {
    switch (activeKey) {
      case 'dashboard':
        return (
          <Row gutter={[16, 16]}>
            <Col span={24}>
              <Card>
                <Row align="middle" justify="space-between">
                  <Col>
                    <Title level={3} style={{ margin: 0 }}>
                      上传会议录音
                    </Title>
                    <p style={{ color: '#666', marginTop: 8 }}>
                      支持 WAV、MP3、M4A、FLAC 格式，系统将自动进行语音转写、说话人分离、分析并生成交易策略
                    </p>
                  </Col>
                  <Col>
                    <Upload {...uploadProps}>
                      <Button type="primary" size="large" icon={<UploadOutlined />} loading={loading}>
                        {loading ? '处理中...' : '上传音频文件'}
                      </Button>
                    </Upload>
                  </Col>
                </Row>
                {progress > 0 && (
                  <Progress percent={progress} style={{ marginTop: 16 }} />
                )}
              </Card>
            </Col>
            <Col span={12}>
              <Card title="碳价走势图" extra={<Button type="link" onClick={() => setActiveKey('price')}>查看详情</Button>}>
                <CarbonPriceChart data={carbonPriceData.slice(-60)} />
              </Card>
            </Col>
            <Col span={12}>
              <Card title="减排曲线图" extra={<Button type="link" onClick={() => setActiveKey('emission')}>查看详情</Button>}>
                <EmissionCurveChart data={emissionData} />
              </Card>
            </Col>
          </Row>
        );
      case 'price':
        return (
          <Card title="碳价K线图">
            <CarbonPriceChart data={carbonPriceData} height={500} />
          </Card>
        );
      case 'emission':
        return (
          <Card title="减排曲线图">
            <EmissionCurveChart data={emissionData} height={500} />
          </Card>
        );
      case 'meeting':
        return meetingData ? <MeetingMinutes data={meetingData} /> : null;
      case 'strategy':
        return meetingData ? <StrategyPanel data={meetingData} /> : null;
      default:
        return null;
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#001529', display: 'flex', alignItems: 'center', padding: '0 24px' }}>
        <Title level={3} style={{ color: '#fff', margin: 0, marginRight: 48 }}>
          碳交易市场策略会系统
        </Title>
        <div style={{ flex: 1 }} />
        {meetingData && (
          <Upload {...uploadProps}>
            <Button icon={<UploadOutlined />}>重新上传</Button>
          </Upload>
        )}
      </Header>
      <Layout>
        <Sider width={200} style={{ background: '#fff' }}>
          <Menu
            mode="inline"
            selectedKeys={[activeKey]}
            onClick={({ key }) => setActiveKey(key)}
            style={{ height: '100%', borderRight: 0 }}
            items={menuItems}
          />
        </Sider>
        <Layout style={{ padding: '24px' }}>
          <Content style={{ background: '#fff', padding: 24, minHeight: 280 }}>
            {renderContent()}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
};

export default App;
