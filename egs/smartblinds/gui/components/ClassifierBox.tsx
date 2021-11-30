import React from 'react'
import { css } from '@emotion/react'
import { ClassifierI } from '../context/TaskContext'
import AnimationPosition from './AnimationPosition'
import AnimationTilt from './AnimationTilt'
import Icon from './atomic/Icon'

const componentS = (updated: boolean) => css({
  display: 'flex',
  flexDirection: 'row',
  marginBottom: '50px',
  padding: '10px',
  border: updated ? '2px solid green' : '2px solid maroon'
})

const classifierInfoS = () => css({
  display: 'flex',
  flexDirection: 'column',
  flexGrow: 1
})

const classifierTitleS = (updated: boolean) => css({
  display: 'flex',
  flexDirection: 'row',
  color: updated ? 'green' : 'maroon',
  fontSize: '22px',
  fontWeight: 'bold',
})

const classifierDescriptionS = () => css({
  display: 'flex',
  flexDirection: 'column',
  color: 'darkgray',
  padding: '7px',
  fontSize: '13px',
  lineHeight: '2em'
})

const classifierOutputS = () => css({
  display: 'flex',
  flexDirection: 'row',
  flexGrow: 0,
  flexBasis: '300px',
  marginLeft: '50px',
  justifyContent: 'space-around'
})

const animationFrameS = () => css({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'space-between'
})

const iconAS = () => css({
  marginRight: '10px'
})

interface ClassifierBoxI {
  classifier: ClassifierI
  classifierInd: number
}

const ClassifierBox: React.FunctionComponent<ClassifierBoxI> = ({ classifier }) => {
  
  return (
    <div css={componentS(classifier.state.sim.updated)}>
      <div css={classifierInfoS}>
        <div css={classifierTitleS(classifier.state.sim.updated)}>
          <Icon iconStyle={iconAS}>update</Icon>
          {classifier.name}
        </div>
        <div css={classifierDescriptionS}>
          <div>
            {classifier.description}
          </div>
          <div>
            {classifier.retrained != 'never' && 'Number of samples: '+classifier.dataTraining.length+' | Retrained: '+classifier.retrained+' | Train time: '+classifier.trainTime}
          </div>
        </div>
      </div>
      <div css={classifierOutputS}>
        <div css={animationFrameS}>
          <AnimationPosition value={classifier.state.sim.position} />
          <div>
            {'Position: '+classifier.state.sim.position}
            </div>
        </div>
        <div css={animationFrameS}>
          <AnimationTilt value={classifier.state.sim.tilt} />
          <div>
            {'Tilt: '+classifier.state.sim.tilt}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ClassifierBox