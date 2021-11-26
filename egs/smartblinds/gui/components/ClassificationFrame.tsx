import React, { useContext } from 'react'
import { css } from '@emotion/react'
import TaskContext, { FeatureI, TargetI } from '../context/TaskContext'

const componentS = () => css({
  flexGrow: 1,
  display: 'flex',
  flexDirection: 'column',
  marginLeft: '50px',
  border: '1px solid blue'
})

const ClassificationFrame: React.FunctionComponent = () => {

  const { features, targets } = useContext(TaskContext)

  return (
    <div css={componentS}>
      {Object.values(targets).map((feature: FeatureI, featureInd: number) => 
        <div key={featureInd}>
          {'Classifier '+featureInd}
        </div>
      )}
    </div>
  )
}

export default ClassificationFrame