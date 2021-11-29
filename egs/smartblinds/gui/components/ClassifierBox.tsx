import React, { useContext, useState } from 'react'
import { css } from '@emotion/react'
import { ClassifierI } from '../context/TaskContext'
import SimulatorContext from '../context/SimulatorContext'

const componentS = () => css({
  display: 'flex',
  flexDirection: 'row',
  marginBottom: '50px',
  border: '1px solid red'
})

interface ClassifierBoxI {
  classifier: ClassifierI
  classifierInd: number
}

const ClassifierBox: React.FunctionComponent<ClassifierBoxI> = ({ classifier, classifierInd }) => {

  const simulatorContext = useContext(SimulatorContext)
  const [updated, setUpdated] = useState(simulatorContext.classifiersUpdated[classifier.name])

  return (
    <div css={componentS}>
      {'Classifier '+classifierInd+' : '+classifier.name+' : '+classifier.description}
    </div>
  )
}

export default ClassifierBox