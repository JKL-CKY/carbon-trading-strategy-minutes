import React from 'react';
import ReactECharts from 'echarts-for-react';
import type { CarbonPriceData } from '../types';

interface CarbonPriceChartProps {
  data: CarbonPriceData[];
  height?: number;
}

const CarbonPriceChart: React.FC<CarbonPriceChartProps> = ({ data, height = 350 }) => {
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
      },
      formatter: function (params: any) {
        const data = params[0];
        return `
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 8px;">${data.name}</div>
            <div>开盘: ${data.data[1]} 元/吨</div>
            <div>收盘: ${data.data[2]} 元/吨</div>
            <div>最低: ${data.data[3]} 元/吨</div>
            <div>最高: ${data.data[4]} 元/吨</div>
          </div>
        `;
      },
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%',
    },
    xAxis: {
      type: 'category',
      data: data.map((item) => item.date),
      axisLabel: {
        rotate: 45,
        fontSize: 10,
      },
    },
    yAxis: {
      scale: true,
      name: '价格 (元/吨)',
      splitArea: {
        show: true,
      },
    },
    dataZoom: [
      {
        type: 'inside',
        start: 50,
        end: 100,
      },
      {
        show: true,
        type: 'slider',
        bottom: 10,
        start: 50,
        end: 100,
      },
    ],
    series: [
      {
        name: '碳价',
        type: 'candlestick',
        data: data.map((item) => [item.open, item.close, item.low, item.high]),
        itemStyle: {
          color: '#ef4444',
          color0: '#22c55e',
          borderColor: '#ef4444',
          borderColor0: '#22c55e',
        },
      },
    ],
  };

  return <ReactECharts option={option} style={{ height }} />;
};

export default CarbonPriceChart;
