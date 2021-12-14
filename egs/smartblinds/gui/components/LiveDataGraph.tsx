import React, { useContext } from 'react'
import { css } from '@emotion/react'
import ReactECharts from 'echarts-for-react-typescript'
import TaskContext, { FeatureI } from '../context/TaskContext'
import DataContext, { DocumentI } from '../context/DataContext'
import LiveContext from '../context/LiveContext'
import Icon from './atomic/Icon'
import { ts2date, norm } from '../fcn/_tools'


const componentS = () => css({
  width: '100%'
})

const chartS = () => css({
  border: '2px solid green'
})

const LiveDataGraph: React.FunctionComponent = () => {

  const { features } = useContext(TaskContext)
  const { documents } = useContext(DataContext)

  const chartsSeries = features.map((feature: FeatureI) => ({
    name: feature.name,
    type: 'line',
    data: documents.map((document: DocumentI) => norm(document.features[feature.name], feature.min, feature.max))
  }))

  const chartsOption = {
    title: {
      text: ''
    },
    tooltip: {
      trigger: 'axis',
      position: (point: Array<number>) => {
          return [point[0], '10%']
      }
    },
    legend: {
      data: features.map((feature: FeatureI) => feature.name)
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
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
      min: -0.1,
      max: 1.1
    },
    series: chartsSeries
  }

  const chartIsReady = () => {
    console.log('Live data chart is ready.')
  }

  const chartClicked = () => {
    console.log('Live data chart clicked.')
  }

  const chartLegendSelectChanged = () => {
    console.log('Live data chart legend select changed.')
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
        theme={"theme_name"}
        onChartReady={chartIsReady}
        onEvents={onEvents}
      />
    </div>
  )
}

export default LiveDataGraph