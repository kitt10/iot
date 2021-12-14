import React, { useContext } from 'react'
import { css } from '@emotion/react'
import ReactECharts from 'echarts-for-react-typescript'
import TaskContext, { TargetI } from '../context/TaskContext'
import DataContext, { DocumentI } from '../context/DataContext'
import { ts2date, norm } from '../fcn/_tools'

const componentS = () => css({
  width: '100%',
  height: '38vh'
})

const chartS = () => css({
  maxHeight: '38vh'
})

const LiveControlGraph: React.FunctionComponent = () => {

  const { targets } = useContext(TaskContext)
  const { documents } = useContext(DataContext)

  const chartsSeries = targets.map((target: TargetI) => ({
    name: 'actual_'+target.name,
    type: 'line',
    symbol: 'roundRect',
    data: documents.map((document: DocumentI) => document.targets[target.name])
  }))

  const chartsOption = {
    title: {
      text: ''
    },
    tooltip: {
      trigger: 'axis',
      position: (point: Array<number>) => {
          return [point[0]+20, '12%']
      }
    },
    legend: {
      data: targets.map((target: TargetI) => 'actual_'+target.name)
    },
    grid: {
      left: '3%',
      right: '3%',
      bottom: '3%',
      top: '12%',
      containLabel: true
    },
    toolbox: {
      show: false
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: documents.map((document: DocumentI) => ts2date(document.timestamp))
    },
    yAxis: {
      type: 'value',
      min: -10,
      max: 110
    },
    series: chartsSeries,
    color: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']
  }

  const chartIsReady = () => {
    console.log('Live control chart is ready.')
  }

  const chartClicked = () => {
    console.log('Live control chart clicked.')
  }

  const chartLegendSelectChanged = () => {
    console.log('Live control chart legend select changed.')
  }

  const onEvents = {
    'click': chartClicked,
    'legendselectchanged': chartLegendSelectChanged
  }

  return (
    <div css={componentS}>
      <ReactECharts
        option={chartsOption}
        css={chartS}
        notMerge={true}
        lazyUpdate={true}
        onChartReady={chartIsReady}
        onEvents={onEvents}
      />
    </div>
  )
}

export default LiveControlGraph