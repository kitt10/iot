import React, { useContext } from 'react'
import { css } from '@emotion/react'
import TaskContext, { FeatureI, TargetI } from '../context/TaskContext'
import Icon from './atomic/Icon'

const componentS = () => css({
  flexGrow: 0,
  display: 'flex',
  flexDirection: 'column',
  fontSize: '12px',
  lineHeight: '2em',
  marginLeft: '50px'
})

const legendLineS = () => css({
  display: 'flex', 
  flexDirection: 'row'
})

const legendIconAS = () => css({
  opacity: 0.7,
  marginRight: '10px',
  marginBottom: '5px'
})

const sepLineS = () => css({
  width: '100%',
  height: '20px',
  borderTop: '2px solid darkgray',
  marginTop: '20px'
})

const DataLegend: React.FunctionComponent = () => {

  const { features, targets } = useContext(TaskContext)

  return (
    <div css={componentS}>
      {Object.values(features).map((feature: FeatureI, featureInd: number) => 
        <div key={featureInd} css={legendLineS}>
          <Icon iconStyle={legendIconAS}>{feature.icon}</Icon>
          {feature.name}
        </div>
      )}
      <div css={sepLineS}>
        &nbsp;
      </div>
      {Object.values(targets).map((target: TargetI, targetInd: number) => 
        <div key={targetInd} css={legendLineS}>
          <Icon iconStyle={legendIconAS}>{target.icon}</Icon>
          {target.name}
      </div>
      )}
    </div>
  )
}

export default DataLegend