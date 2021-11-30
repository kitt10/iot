import React, { useContext, useEffect, useState } from 'react'
import { css } from '@emotion/react'
import TaskContext, { ClassifierI } from '../context/TaskContext'
import SimulatorContext from '../context/SimulatorContext'
import Icon from './atomic/Icon'

const componentS = (updated: boolean) => css({
  display: 'flex',
  flexDirection: 'row',
  marginBottom: '50px',
  padding: '10px',
  border: updated ? '1px dotted green' : '1px dotted maroon'
})

const classifierInfoS = () => css({
  display: 'flex',
  flexDirection: 'column',
  flexBasis: '70%',
  flexGrow: 1,
  border: '1px solid darkblue'
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
  fontSize: '13px'
})

interface ClassifierBoxI {
  classifier: ClassifierI
  classifierInd: number
}

const ClassifierBox: React.FunctionComponent<ClassifierBoxI> = ({ classifier, classifierInd }) => {

  const simulatorContext = useContext(SimulatorContext)
  const taskContext = useContext(TaskContext)
  
  return (
    <div css={componentS(classifier.state.sim.updated)}>
      <div css={classifierInfoS}>
        <div css={classifierTitleS(classifier.state.sim.updated)}>
          <Icon>update</Icon>
          {classifier.name}
        </div>
        <div css={classifierDescriptionS}>
          {classifier.description}
        </div>
      </div>
    </div>
  )
}

export default ClassifierBox