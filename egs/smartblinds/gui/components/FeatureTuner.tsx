import React, { useContext } from 'react'
import { css } from '@emotion/react'
import TaskContext, { FeatureI, TargetI } from '../context/TaskContext'

const componentS = () => css({
  flexGrow: 0,
  flexBasis: 'fit-content',
  display: 'flex',
  flexDirection: 'column',
  border: '1px solid green'
})

const FeatureTuner: React.FunctionComponent = () => {

  const { features, targets } = useContext(TaskContext)

  return (
    <div css={componentS}>
      {Object.values(features).map((feature: FeatureI, featureInd: number) => 
        <div key={featureInd}>
          {'F'+(featureInd+1)+': '+feature.name}
        </div>
      )}
    </div>
  )
}

export default FeatureTuner