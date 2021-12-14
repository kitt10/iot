import React, { useContext } from 'react'
import { css } from '@emotion/react'
import ReactECharts from 'echarts-for-react-typescript'
import TaskContext, { FeatureI } from '../context/TaskContext'
import DataContext, { DocumentI } from '../context/DataContext'
import LiveContext from '../context/LiveContext'
import { ts2date } from '../fcn/_tools'


const componentS = () => css({
  width: '100%'
})

const chartS = () => css({
  border: '2px solid green'
})

const LiveDataGraph: React.FunctionComponent = () => {

  const { features } = useContext(TaskContext)
  const { documents } = useContext(DataContext)

  const chartsOption = {
    title: {
      text: 'Data'
    },
    tooltip: {
      trigger: 'axis'
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
      feature: {
        saveAsImage: {}
      }
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: documents.map((document: DocumentI) => ts2date(document.timestamp))
    },
    yAxis: {
      type: 'value'
    },
    series: features.map((feature: FeatureI) => ({
      name: feature.name,
      type: 'line',
      stack: 'Total',
      data: documents.map((document: DocumentI) => document.features[feature.name])
    }))
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