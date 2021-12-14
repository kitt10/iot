import React, { useContext } from 'react'
import { css } from '@emotion/react'
import ReactECharts from 'echarts-for-react-typescript'
import TaskContext, { FeatureI } from '../context/TaskContext'
import DataContext, { DocumentI } from '../context/DataContext'
import { ts2date, norm } from '../fcn/_tools'

const componentS = () => css({
  width: '100%',
  height: '40vh'
})

const chartS = () => css({
  
})

const LiveDataGraph: React.FunctionComponent = () => {

  const { features } = useContext(TaskContext)
  const { documents } = useContext(DataContext)

  const chartsSeries = features.map((feature: FeatureI) => ({
    name: feature.name,
    type: 'line',
    data: documents.map((document: DocumentI) => norm(document.features[feature.name], feature.min, feature.max))
  }))

  const selected = features.reduce((a: FeatureI, feature: FeatureI) => ({ ...a, [feature.name]: feature.show}), {} as FeatureI)

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
      data: features.map((feature: FeatureI) => feature.name),
      selected: selected
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
        onChartReady={chartIsReady}
        onEvents={onEvents}
      />
    </div>
  )
}

export default LiveDataGraph