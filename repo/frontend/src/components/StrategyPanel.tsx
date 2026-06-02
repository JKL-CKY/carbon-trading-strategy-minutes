import React from 'react';
import { Row, Col, Card, List, Tag, Progress, Space, Typography } from 'antd';
import {
  ArrowUpOutlined,
  ArrowDownOutlined,
  SafetyOutlined,
  ClockCircleOutlined,
  FundOutlined,
  AlertOutlined,
} from '@ant-design/icons';
import type { MeetingResponse } from '../types';

const { Title, Paragraph } = Typography;

interface StrategyPanelProps {
  data: MeetingResponse;
}

const StrategyPanel: React.FC<StrategyPanelProps> = ({ data }) => {
  const strategy = data.trading_strategy;

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return '#52c41a';
    if (confidence >= 0.6) return '#faad14';
    return '#ff4d4f';
  };

  return (
    <div>
      <Card style={{ marginBottom: 16 }}>
        <Row align="middle" gutter={[16, 16]}>
          <Col flex="auto">
            <Title level={3} style={{ margin: 0, marginBottom: 8 }}>
              交易策略建议
            </Title>
            <Paragraph style={{ margin: 0, fontSize: 15, lineHeight: 1.8 }}>
              {strategy.strategy_summary}
            </Paragraph>
          </Col>
          <Col flex="120px">
            <div style={{ textAlign: 'center' }}>
              <Title level={5} style={{ marginBottom: 8 }}>
                策略置信度
              </Title>
              <Progress
                type="circle"
                percent={Math.round(strategy.confidence_level * 100)}
                strokeColor={getConfidenceColor(strategy.confidence_level)}
                width={80}
              />
            </div>
          </Col>
        </Row>
      </Card>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card
            title={
              <Space>
                <ArrowUpOutlined style={{ color: '#52c41a' }} />
                入场点位建议
              </Space>
            }
            style={{ borderTop: '3px solid #52c41a' }}
          >
            <List
              dataSource={strategy.entry_points}
              renderItem={(item, index) => (
                <List.Item>
                  <Tag color="green" style={{ minWidth: 30, textAlign: 'center' }}>
                    {index + 1}
                  </Tag>
                  <span style={{ flex: 1 }}>{item}</span>
                </List.Item>
              )}
            />
          </Card>
        </Col>

        <Col span={12}>
          <Card
            title={
              <Space>
                <ArrowDownOutlined style={{ color: '#ff4d4f' }} />
                出场点位建议
              </Space>
            }
            style={{ borderTop: '3px solid #ff4d4f' }}
          >
            <List
              dataSource={strategy.exit_points}
              renderItem={(item, index) => (
                <List.Item>
                  <Tag color="red" style={{ minWidth: 30, textAlign: 'center' }}>
                    {index + 1}
                  </Tag>
                  <span style={{ flex: 1 }}>{item}</span>
                </List.Item>
              )}
            />
          </Card>
        </Col>

        <Col span={12}>
          <Card
            title={
              <Space>
                <FundOutlined style={{ color: '#1890ff' }} />
                仓位管理
              </Space>
            }
          >
            <p style={{ lineHeight: 1.8, margin: 0 }}>{strategy.position_sizing}</p>
          </Card>
        </Col>

        <Col span={12}>
          <Card
            title={
              <Space>
                <SafetyOutlined style={{ color: '#fa8c16' }} />
                风险管理
              </Space>
            }
          >
            <p style={{ lineHeight: 1.8, margin: 0 }}>{strategy.risk_management}</p>
          </Card>
        </Col>

        <Col span={24}>
          <Card
            title={
              <Space>
                <ClockCircleOutlined style={{ color: '#722ed1' }} />
                操作时间周期
              </Space>
            }
          >
            <p style={{ lineHeight: 1.8, margin: 0, fontSize: 15 }}>{strategy.time_horizon}</p>
          </Card>
        </Col>

        <Col span={24}>
          <Card
            title={
              <Space>
                <AlertOutlined style={{ color: '#eb2f96' }} />
                买卖双方博弈要点
              </Space>
            }
          >
            <Row gutter={[16, 16]}>
              <Col span={12}>
                <Title level={5} style={{ color: '#ef4444', marginBottom: 12 }}>
                  买方核心诉求
                </Title>
                <List
                  dataSource={data.buyer_viewpoints}
                  renderItem={(item) => (
                    <List.Item>
                      <Tag color="red">买方</Tag>
                      {item}
                    </List.Item>
                  )}
                />
              </Col>
              <Col span={12}>
                <Title level={5} style={{ color: '#22c55e', marginBottom: 12 }}>
                  卖方核心诉求
                </Title>
                <List
                  dataSource={data.seller_viewpoints}
                  renderItem={(item) => (
                    <List.Item>
                      <Tag color="green">卖方</Tag>
                      {item}
                    </List.Item>
                  )}
                />
              </Col>
            </Row>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default StrategyPanel;
