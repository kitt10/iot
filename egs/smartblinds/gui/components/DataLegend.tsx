import React, { useContext } from 'react'
import { css } from '@emotion/react'
import TaskContext, { FeatureI, TargetI } from '../context/TaskContext'

const componentS = () => css({
  flexGrow: 0,
  display: 'flex',
  flexDirection: 'column',
  fontSize: '12px',
  lineHeight: '2em',
  marginLeft: '50px'
})

const DataLegend: React.FunctionComponent = () => {

  const { features, targets } = useContext(TaskContext)

  return (
    <div css={componentS}>
      {Object.values(features).map((feature: FeatureI, featureInd: number) => 
        <div key={featureInd}>
          {'F'+(featureInd+1)+': '+feature.name}
        </div>
      )}
      {Object.values(targets).map((target: TargetI, targetInd: number) => 
        <div key={targetInd}>
          {'T'+(targetInd+1)+': '+target.name}
        </div>
      )}
    </div>
  )
}

export default DataLegend