import React, { useContext } from 'react'
import { css } from '@emotion/react'
import Button from './atomic/Button'
import TaskContext from '../context/TaskContext'

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

  const { taskInfo } = useContext(TaskContext)

  const clickHandler = () => {
    console.log('button clicked')
  }

  return (
    <div css={componentS}>
      <Button text='Retrain classifiers now'
              onClick={clickHandler}
              buttonStyle={buttonAS} />

      <div css={infoTextS}>
        {'Next retraining planned to '+taskInfo.nextTraining}
      </div>
    </div>
  )
}

export default ClassificationControls