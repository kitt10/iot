import React, { useContext } from 'react'
import { css } from '@emotion/react'

const componentS = () => css({
  flexGrow: 0,
  width: '50px',
  height: '50px',
  marginBottom: '10px',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: '#ddd',
  border: '1px solid darkgray',
  borderRadius: '50%'
})

const blindsS = (value: number) => css({
  backgroundColor: 'black',
  width: '100%',
  height: '5px',
  transform: `rotate(${value}deg)`    // TO BE CALIBRATED
})

interface AnimationTiltI {
  value: number
}

const AnimationTilt: React.FunctionComponent<AnimationTiltI> = ({ value }) => {


  return (
    <div css={componentS}>
      <div css={blindsS(value)}>
        &nbsp;
      </div>
    </div>
  )
}

export default AnimationTilt