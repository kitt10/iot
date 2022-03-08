import React, { useContext } from 'react'
import { css } from '@emotion/react'
import ReactECharts from 'echarts-for-react-typescript'
import TaskContext, { ClassifierI, TargetI } from '../context/TaskContext'
import DataContext, { DocumentI, PredictionI } from '../context/DataContext'
import { ts2date, norm } from '../fcn/_tools'

const componentS = () => css({
  width: '100%',
  height: '38vh'
})

const chartS = () => css({
  maxHeight: '38vh'
})

interface formatterParam {
    componentType: 'series',
    // Series type
    seriesType: string,
    // Series index in option.series
    seriesIndex: number,
    // Series name
    seriesName: string,
    // Data name, or category name
    name: string,
    // Data index in input data array
    dataIndex: number,
    // Original data as input
    data: Object,
    // Value of data. In most series it is the same as data.
    // But in some series it is some part of the data (e.g., in map, radar)
    value: Array<number>,
    // encoding info of coordinate system
    // Key: coord, like ('x' 'y' 'radius' 'angle')
    // value: Must be an array, not null/undefined. Contain dimension indices, like:
    // {
    //     x: [2] // values on dimension index 2 are mapped to x axis.
    //     y: [0] // values on dimension index 0 are mapped to y axis.
    // }
    encode: Object,
    // dimension names list
    dimensionNames: Array<String>,
    // data dimension index, for example 0 or 1 or 2 ...
    // Only work in `radar` series.
    dimensionIndex: number,
    // Color of data
    color: string
}

const LiveControlGraph: React.FunctionComponent = () => {

  const { targets, classifiers } = useContext(TaskContext)
  const { documents, predictions } = useContext(DataContext)

  var chartsSeries = targets.map((target: TargetI) => ({
    name: 'actual_'+target.name,
    type: 'line',
    symbol: 'roundRect',
    encode: {
      x: 0,
      y: 1
    },
    data: documents.map((document: DocumentI) => [1000*document.timestamp, document.targets[target.name]])
  }))

  let classfs = [classifiers[0]]

  let predictedSeries = classfs.map((cl: ClassifierI) => (targets.map((target: TargetI) => ({
    name: cl.name + '_' + target.name,
    type: 'line',
    symbol: 'roundRect',
    encode: {
      x: 0,
      y: 1
    },
    data: predictions[cl.name]['predictions'].map((prediction: PredictionI) => [1000*prediction.timestamp, prediction.targets[target.name]])
  }))))

  for (let p of predictedSeries){
    for(let t of p)
    chartsSeries.push(t)
  }

  console.log(chartsSeries)

  const chartsOption = {
    title: {
      text: ''
    },
    tooltip: {
      trigger: 'axis',
      position: (point: Array<number>) => {
          return [point[0]+20, '12%']
      },
      formatter: (params: Array<formatterParam>) => {
        let output = `${ts2date(params[0].value[0]/1000)}`
        params.forEach(p => {
          output += `<br /><span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:${p.color}"></span>${p.seriesName}: ${p.value[1]}`
        });
        return output
      }
    },
    legend: {
      data: chartsSeries.map((s) => s.name)
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
      type: 'time',
      axisLabel: {
        formatter: (value:number, index:number) => {return ts2date(value/1000)
        },
      },
      interval: (documents[documents.length-1].timestamp - documents[0].timestamp)/10 * 1000
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