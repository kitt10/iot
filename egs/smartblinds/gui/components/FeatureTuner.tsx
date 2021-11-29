import React from 'react'
import { css } from '@emotion/react'
import { FeatureI } from '../context/TaskContext'

const componentS = () => css({
  lineHeight: '1.7em'
})

interface FeatureTunerI {
  feature: FeatureI
  featureInd: number
}

const FeatureTuner: React.FunctionComponent<FeatureTunerI> = ({ feature, featureInd }) => {

  return (
    <div css={componentS}>
      {'F'+(featureInd+1)+': '+feature.name}
    </div>
  )
}

export default FeatureTuner