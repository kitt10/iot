import React, { useContext } from 'react'
import { css } from '@emotion/react'
import { trainAll } from '../fcn/clientSide'
import { ts2date } from '../fcn/_tools'
import TaskContext from '../context/TaskContext'
import Slider from './atomic/Slider'
import Button from './atomic/Button'
import DataContext from '../context/DataContext'
import config from '../config'

const componentS = () => css({
  flexGrow: 1,
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'center',
  alignItems: 'center'
})

const buttonAS = () => css({
  width: 'fit-content',
  padding: '7px',
  border: '1px solid darkgray',
  borderRadius: '5px'
})

const tBackControlsS = () => css({
  display: 'flex',
  flexDirection: 'column',
  marginRight: '50px'
})

const tBackControlsLineS = () => css({
  display: 'flex',
  flexDirection: 'row',
  justifyItems: 'flex-end',
  alignItems: 'center',
  fontSize: '12px',
  whiteSpace: 'nowrap'
})

const tBackControlsSliderS = () => css({
  width: 'fit-content'
})

const tBackControlsTextS = () => css({
  marginLeft: '10px',
  marginRight: '10px',
  minWidth: '80px'
})

const ControlPanel: React.FunctionComponent = () => {

  const { classifiers, setClassifiers } = useContext(TaskContext)
  const { trainBack, setTrainBack, showBack, setShowBack } = useContext(DataContext)

  const inpTrainBackRef: React.RefObject<HTMLInputElement> = React.createRef<HTMLInputElement>()
  const inpShowBackRef: React.RefObject<HTMLInputElement> = React.createRef<HTMLInputElement>()
  const now: number = + new Date() / 1000

  const clickHandler = async () => {
    let clInfo = await trainAll()
    for (let cl of classifiers) {
      cl.retrained = clInfo[cl.name].lastTrained
      cl.trainTime = clInfo[cl.name].trainTime
      cl.nSamples = clInfo[cl.name].nSamples
    }
    setClassifiers([...classifiers])
  }

  const changeTrainBackHandler = () => {
    if (inpTrainBackRef.current) {
      setTrainBack(+inpTrainBackRef.current.value)
    }
  }

  const changeShowBackHandler = () => {
    if (inpShowBackRef.current) {
      setShowBack(+inpShowBackRef.current.value)
    }
  }

  return (
    <div css={componentS}>
      <div css={tBackControlsS}>
        <div css={tBackControlsLineS}>
          <div css={tBackControlsTextS}>
            {'Train back to: '}
          </div>
          <Slider onChange={changeTrainBackHandler} containerStyle={tBackControlsSliderS} sliderRef={inpTrainBackRef} min={config.defaultTrainBack} max={now} defaultValue={trainBack} step={300} />
          <div css={tBackControlsTextS}>
              {ts2date(trainBack)}
          </div>
        </div>
        <div css={tBackControlsLineS}>
          <div css={tBackControlsTextS}>
              {'Show back to: '}
          </div>
          <Slider onChange={changeShowBackHandler} containerStyle={tBackControlsSliderS} sliderRef={inpShowBackRef} min={config.defaultTrainBack} max={now} defaultValue={showBack} step={300} />
          <div css={tBackControlsTextS}>
            {ts2date(showBack)}
          </div>
        </div>
      </div>
      <Button text='Retrain classifiers now'
              onClick={clickHandler}
              buttonStyle={buttonAS} />
    </div>
  )
}

export default ControlPanel