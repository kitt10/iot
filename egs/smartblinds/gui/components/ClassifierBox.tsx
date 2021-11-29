import React from 'react'
import { css } from '@emotion/react'
import { ClassifierI } from '../context/TaskContext'

const componentS = () => css({
  flexGrow: 1,
  display: 'flex',
  flexDirection: 'column',
  marginLeft: '50px',
  border: '1px solid blue'
})

interface ClassifierBoxI {
  classifier: ClassifierI
  classifierInd: number
}

const ClassifierBox: React.FunctionComponent<ClassifierBoxI> = ({ classifier, classifierInd }) => {

  return (
    <div css={componentS}>
      {'Classifier '+classifierInd+' : '+classifier.name+' : '+classifier.description}
    </div>
  )
}

export default ClassifierBox