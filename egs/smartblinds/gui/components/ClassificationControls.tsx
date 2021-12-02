import React, { useContext } from 'react'
import { css } from '@emotion/react'
import { trainAll } from '../fcn/clientSide'
import { ts2date } from '../fcn/_tools'
import TaskContext from '../context/TaskContext'
import Button from './atomic/Button'

const componentS = () => css({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  marginTop: 'auto',
  marginBottom: '50px'
})

const buttonAS = () => css({
  width: 'fit-content',
  padding: '7px',
  border: '1px solid darkgray',
  borderRadius: '5px'
})

const infoTextS = () => css({
  width: 'fit-content',
  color: 'darkgray',
  fontSize: '12px',
  marginTop: '25px'
})

const ClassificationControls: React.FunctionComponent = () => {

  const { taskInfo, classifiers, setClassifiers } = useContext(TaskContext)

  const clickHandler = async () => {
    let clInfo = await trainAll()
    for (let cl of classifiers) {
      cl.retrained = clInfo[cl.name].lastTrained
      cl.trainTime = clInfo[cl.name].trainTime
      cl.nSamples = clInfo[cl.name].nSamples
    }
    setClassifiers([...classifiers])
  }

  return (
    <div css={componentS}>
      <Button text='Retrain classifiers now'
              onClick={clickHandler}
              buttonStyle={buttonAS} />

      <div css={infoTextS}>
        {'Next retraining planned to '+ts2date(taskInfo.nextTraining)}
      </div>
    </div>
  )
}

export default ClassificationControls