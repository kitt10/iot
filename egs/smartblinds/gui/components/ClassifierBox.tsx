import React, { useContext, useEffect, useState } from 'react'
import { css } from '@emotion/react'
import { ClassifierI } from '../context/TaskContext'
import SimulatorContext from '../context/SimulatorContext'

const componentS = (updated: boolean) => css({
  display: 'flex',
  flexDirection: 'row',
  marginBottom: '50px',
  backgroundColor: updated ? 'lime' : 'pink',
  border: '1px solid red'
})

interface ClassifierBoxI {
  classifier: ClassifierI
  classifierInd: number
}

const ClassifierBox: React.FunctionComponent<ClassifierBoxI> = ({ classifier, classifierInd }) => {

  const simulatorContext = useContext(SimulatorContext)
  const [updated, setUpdated] = useState(classifier.state.simUpdated)

  useEffect(() => {
    setUpdated(classifier.state.simUpdated)
    console.log('changed.')
  }, [classifier.state.simUpdated])

  return (
    <div css={componentS(updated)}>
      {'Classifier '+classifierInd+' : '+classifier.name+' : '+classifier.description}
    </div>
  )
}

export default ClassifierBox