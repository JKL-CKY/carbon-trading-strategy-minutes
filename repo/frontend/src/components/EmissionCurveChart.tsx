import React from 'react';
import ReactECharts from 'echarts-for-react';
import type { EmissionData } from '../types';

interface EmissionCurveChartProps {
  data: EmissionData[];
  height?: number;
}

const EmissionCurveChart: React.FC<EmissionCurveChartProps> = ({ data, height = 350 }) => {
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: function (params: any) {
        let html = `<div style="padding: 8px;"><div style="font-weight: bold; margin-bottom: 8px;">${params[0].name}年</div>`;
        params.forEach((item: any) => {
          const unit = item.seriesName === '减排率' ? '%' : ' 百万吨';
          html += `<div>${item.marker} ${item.seriesName}: ${item.value}${unit}</div>`;
        });
        html += '</div>';
        return html;
      },
    },
    legend: {
      data: ['基准排放', '目标排放', '实际排放', '减排率'],
      top: 0,
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '10%',
      top: '15%',
    },
    xAxis: {
      type: 'category',
      data: data.map((item) => item.year),
      name: '年份',
    },
    yAxis: [
      {
        type: 'value',
        name: '排放量 (百万吨)',
        position: 'left',
      },
      {
        type: 'value',
        name: '减排率 (%)',
        position: 'right',
        axisLabel: {
          formatter: '{value}%',
        },
      },
    ],
    series: [
      {
        name: '基准排放',
        type: 'line',
        data: data.map((item) => item.baseline),
        lineStyle: {
          type: 'dashed',
        },
        symbol: 'circle',
        symbolSize: 8,
      },
      {
        name: '目标排放',
        type: 'line',
        data: data.map((item) => item.target),
        lineStyle: {
          type: 'dotted',
        },
        symbol: 'square',
        symbolSize: 8,
      },
      {
        name: '实际排放',
        type: 'line',
        data: data.map((item) => item.actual),
        smooth: true,
        symbol: 'diamond',
        symbolSize: 10,
        itemStyle: {
          color: '#3b82f6',
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
              { offset: 1, color: 'rgba(59, 130, 246, 0.05)' },
            ],
          },
        },
      },
      {
        name: '减排率',
        type: 'bar',
        yAxisIndex: 1,
        data: data.map((item) => item.reduction_rate),
        itemStyle: {
          color: '#10b981',
        },
      },
    ],
  };

  return <ReactECharts option={option} style={{ height }} />;
};

export default EmissionCurveChart;
