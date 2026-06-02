import React, { useState } from 'react';
import {
  Row,
  Col,
  Card,
  Tabs,
  List,
  Tag,
  Descriptions,
  Button,
  Modal,
  Form,
  Input,
  message,
  Space,
} from 'antd';
import { MailOutlined, CopyOutlined } from '@ant-design/icons';
import type { MeetingResponse } from '../types';
import { meetingApi } from '../services/api';
import dayjs from 'dayjs';

interface MeetingMinutesProps {
  data: MeetingResponse;
}

const MeetingMinutes: React.FC<MeetingMinutesProps> = ({ data }) => {
  const [emailModalVisible, setEmailModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [sendingEmail, setSendingEmail] = useState(false);

  const getRoleColor = (role: string) => {
    switch (role) {
      case '买方':
        return 'red';
      case '卖方':
        return 'green';
      case '分析师':
        return 'blue';
      default:
        return 'default';
    }
  };

  const handleSendEmail = async () => {
    try {
      const values = await form.validateFields();
      setSendingEmail(true);

      const recipients = values.recipients.split(',').map((e: string) => e.trim());

      await meetingApi.sendEmail({
        recipients,
        subject: values.subject,
        markdown_content: data.markdown_report,
      });

      message.success('邮件发送成功');
      setEmailModalVisible(false);
      form.resetFields();
    } catch (error) {
      message.error('邮件发送失败');
    } finally {
      setSendingEmail(false);
    }
  };

  const handleCopyReport = async () => {
    try {
      await navigator.clipboard.writeText(data.markdown_report);
      message.success('报告已复制到剪贴板');
    } catch (error) {
      message.error('复制失败');
    }
  };

  const tabItems = [
    {
      key: 'transcript',
      label: '会议转写',
      children: (
        <Card>
          <List
            dataSource={data.transcript_segments}
            renderItem={(segment) => (
              <List.Item
                style={{
                  borderBottom: '1px solid #f0f0f0',
                  padding: '16px 0',
                }}
              >
                <List.Item.Meta
                  title={
                    <Space>
                      <span style={{ color: '#666', fontSize: 12 }}>
                        {dayjs(segment.start_time * 1000).format('mm:ss')} -{' '}
                        {dayjs(segment.end_time * 1000).format('mm:ss')}
                      </span>
                      <Tag color={getRoleColor(segment.speaker_role)}>
                        {segment.speaker_role}
                      </Tag>
                      <span style={{ fontWeight: 500 }}>{segment.speaker}</span>
                    </Space>
                  }
                  description={segment.text}
                />
              </List.Item>
            )}
          />
        </Card>
      ),
    },
    {
      key: 'analysis',
      label: '分析汇总',
      children: (
        <Row gutter={[16, 16]}>
          <Col span={12}>
            <Card title="政策分析">
              <p style={{ lineHeight: 1.8 }}>{data.policy_analysis}</p>
            </Card>
          </Col>
          <Col span={12}>
            <Card title="供需分析">
              <p style={{ lineHeight: 1.8 }}>{data.supply_demand_analysis}</p>
            </Card>
          </Col>
          <Col span={12}>
            <Card title="买方观点" style={{ borderTop: '3px solid #ef4444' }}>
              <List
                dataSource={data.buyer_viewpoints}
                renderItem={(item) => (
                  <List.Item>
                    <Tag color="red">买</Tag>
                    {item}
                  </List.Item>
                )}
              />
            </Card>
          </Col>
          <Col span={12}>
            <Card title="卖方观点" style={{ borderTop: '3px solid #22c55e' }}>
              <List
                dataSource={data.seller_viewpoints}
                renderItem={(item) => (
                  <List.Item>
                    <Tag color="green">卖</Tag>
                    {item}
                  </List.Item>
                )}
              />
            </Card>
          </Col>
        </Row>
      ),
    },
    {
      key: 'report',
      label: '完整报告',
      children: (
        <Card
          extra={
            <Space>
              <Button icon={<CopyOutlined />} onClick={handleCopyReport}>
                复制报告
              </Button>
              <Button
                type="primary"
                icon={<MailOutlined />}
                onClick={() => setEmailModalVisible(true)}
              >
                发送邮件
              </Button>
            </Space>
          }
        >
          <pre
            style={{
              background: '#f5f5f5',
              padding: 16,
              borderRadius: 4,
              whiteSpace: 'pre-wrap',
              fontFamily: 'monospace',
              fontSize: 13,
              lineHeight: 1.6,
            }}
          >
            {data.markdown_report}
          </pre>
        </Card>
      ),
    },
  ];

  return (
    <div>
      <Card style={{ marginBottom: 16 }}>
        <Descriptions title="会议信息" bordered column={3}>
          <Descriptions.Item label="会议ID">{data.meeting_id}</Descriptions.Item>
          <Descriptions.Item label="处理时间">
            {dayjs(data.timestamp).format('YYYY-MM-DD HH:mm:ss')}
          </Descriptions.Item>
          <Descriptions.Item label="发言段数">
            {data.transcript_segments.length} 段
          </Descriptions.Item>
        </Descriptions>
      </Card>

      <Tabs items={tabItems} />

      <Modal
        title="发送会议纪要邮件"
        open={emailModalVisible}
        onOk={handleSendEmail}
        onCancel={() => setEmailModalVisible(false)}
        confirmLoading={sendingEmail}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="subject"
            label="邮件主题"
            initialValue={`碳交易策略会纪要 - ${dayjs(data.timestamp).format('YYYY年MM月DD日')}`}
            rules={[{ required: true, message: '请输入邮件主题' }]}
          >
            <Input placeholder="请输入邮件主题" />
          </Form.Item>
          <Form.Item
            name="recipients"
            label="收件人"
            rules={[{ required: true, message: '请输入收件人邮箱' }]}
            help="多个邮箱用逗号分隔"
          >
            <Input placeholder="invest@company.com, analyst@company.com" />
          </Form.Item>
          <Form.Item label="附件内容">
            <Input.TextArea
              value={data.markdown_report}
              rows={8}
              readOnly
              style={{ fontFamily: 'monospace', fontSize: 12 }}
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default MeetingMinutes;
