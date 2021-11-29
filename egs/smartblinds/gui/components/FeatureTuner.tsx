import React, { useContext, useState } from 'react'
import { css } from '@emotion/react'
import { FeatureI } from '../context/TaskContext'
import SimulatorContext from '../context/SimulatorContext'
import Slider from './atomic/Slider'
import CheckBox from './atomic/CheckBox'

const componentS = () => css({
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'space-between',
  alignItems: 'center',
  padding: '5px',
  border: '1px solid lightgray'
})

const tunerHeaderS = () => css({
  fontSize: '12px'
})

const tunerControlS = () => css({
  marginLeft: '15px',
  width: '200px',
  display: 'flex',
  flexDirection: 'row'
})

interface FeatureTunerI {
  feature: FeatureI
  featureInd: number
}

const FeatureTuner: React.FunctionComponent<FeatureTunerI> = ({ feature, featureInd }) => {

  const simulatorContext = useContext(SimulatorContext)
  const [featureValue, setFeatureValue] = useState(simulatorContext.simFeatureVector[feature.name])
  const inpRef: React.RefObject<HTMLInputElement> = React.createRef<HTMLInputElement>()

  const changeHandler = () => {
    if (inpRef.current) {
      if (feature.type == 'int' || feature.type == 'float') {
        simulatorContext.updateSimFeatureVector(feature.name, +inpRef.current.value)
      } else if (feature.type == 'boolean') {
        simulatorContext.updateSimFeatureVector(feature.name, inpRef.current.checked)
      }
      setFeatureValue(simulatorContext.simFeatureVector[feature.name])
    }
  }

  return (
    <div css={componentS}>
      <div css={tunerHeaderS} >
        {'F'+(featureInd+1)+': '+feature.name}
      </div>
      <div css={tunerControlS}>
        {feature.type == 'float' && <Slider onChange={changeHandler} sliderRef={inpRef} min={feature.min || 0} max={feature.max || 1} defaultValue={featureValue.toString()} step={0.1} />}
        {feature.type == 'int' && <Slider onChange={changeHandler} sliderRef={inpRef} min={feature.min || 0} max={feature.max || 1} defaultValue={featureValue.toString()} step={1} />}
        {feature.type == 'boolean' && <CheckBox onChange={changeHandler} checkboxRef={inpRef} labelText={featureValue.toString()} />}
        {featureValue}
      </div>
    </div>
  )
}

export default FeatureTuner