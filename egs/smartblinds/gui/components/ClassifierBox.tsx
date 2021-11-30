import React, { useContext, useEffect, useState } from 'react'
import { css } from '@emotion/react'
import TaskContext, { ClassifierI } from '../context/TaskContext'
import SimulatorContext from '../context/SimulatorContext'

const componentS = (updated: boolean) => css({
  display: 'flex',
  flexDirection: 'row',
  marginBottom: '50px',
  border: updated ? '1px solid green' : '1px solid maroon'
})

interface ClassifierBoxI {
  classifier: ClassifierI
  classifierInd: number
}

const ClassifierBox: React.FunctionComponent<ClassifierBoxI> = ({ classifier, classifierInd }) => {

  const simulatorContext = useContext(SimulatorContext)
  const taskContext = useContext(TaskContext)
  const [updated, setUpdated] = useState(classifier.state.sim.updated)

  useEffect(() => {
    setUpdated(classifier.state.sim.updated)
  }, [taskContext.classifiers])

  return (
    <div css={componentS(updated)}>
      {'Classifier '+classifierInd+' : '+classifier.name+' : '+classifier.description}
    </div>
  )
}

export default ClassifierBox