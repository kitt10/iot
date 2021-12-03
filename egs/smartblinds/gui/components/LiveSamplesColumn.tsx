import React, { useContext } from 'react'
import { css } from '@emotion/react'
import { ts2date } from '../fcn/_tools'
import LiveContext from '../context/LiveContext'
import DataContext, { DocumentI } from '../context/DataContext'
import TaskContext, { FeatureI } from '../context/TaskContext'


const componentS = (relativeWidth: number) => css({
  flexBasis: relativeWidth < 1 ? '1%' : `${relativeWidth}%`,
  maxWidth: relativeWidth < 1 ? '1%' : `${relativeWidth}%`,
  display: 'flex',
  flexDirection: 'column',
  cursor: 'crosshair'
})

const featureValueFrameS = (lineNb: number) => css({
  flexBasis: '6.6%',
  width: '100%',
  backgroundColor: lineNb % 2 == 0 ? '#ddd' : '#fff',
  ':hover': {
    backgroundColor: 'lime'
  }
})

const featureValueLineS = (value: number) => css({
  position: 'relative',
  top: `${value}%`,
  height: '1px',
  width: '100%',
  backgroundColor: 'black'
})

interface FeatureValueFrameI {
  doc: DocumentI
  feature: FeatureI
  featureInd: number
}

const FeatureValueFrame: React.FunctionComponent<FeatureValueFrameI> = ({ doc, feature, featureInd }) => {

  const { updateSamplesTitle } = useContext(LiveContext)

  const normalizedValue = (value: number | boolean, a_min: number | undefined, a_max: number | undefined) => {
    if (typeof value === 'number' && a_min && a_max) {
      return ((value-a_min)/(a_max-a_min))*100
    } else {
      return value ? 100 : 0
    }
  }

  return (
      <div css={featureValueFrameS(featureInd)} onMouseOver={() => updateSamplesTitle(doc, feature)}>
        <div css={featureValueLineS(normalizedValue(doc.features[feature.name], feature.min, feature.max))}>
          &nbsp;
        </div>
      </div>
  )
}

interface LiveSampleColumnI {
  doc: DocumentI
  docInd: number
  nDocs: number
}

const LiveSampleColumn: React.FunctionComponent<LiveSampleColumnI> = ({ doc,  nDocs }) => {
  
  const { features } = useContext(TaskContext)
  const { showBack } = useContext(DataContext)

  const relativeWidth: number = 100 / nDocs
  
  return (
    <div css={componentS(relativeWidth)}>
      {Object.values(features).map((feature: FeatureI, featureInd: number) => 
        <FeatureValueFrame key={'featureValueFrame_'+featureInd} doc={doc} feature={feature} featureInd={featureInd} />
      )}
    </div>
  )
}

export default React.memo(LiveSampleColumn)