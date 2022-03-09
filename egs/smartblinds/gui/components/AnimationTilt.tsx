import React, { useContext } from 'react'
import { css } from '@emotion/react'
import { createMap } from '../fcn/_tools'

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

const tilt2angle = createMap(100, 0, 0, 90);

const blindsS = (value: number) => css({
  backgroundColor: 'black',
  width: '100%',
  height: '5px',
  transform: `rotate(${tilt2angle(value)}deg)`
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