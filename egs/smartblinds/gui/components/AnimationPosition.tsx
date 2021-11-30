import React from 'react'
import { css } from '@emotion/react'

const componentS = () => css({
  flexGrow: 0,
  width: '50px',
  height: '50px',
  marginBottom: '10px',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  backgroundColor: '#ddd',
  border: '1px solid black'
})

const blindsS = (value: number) => css({
  backgroundColor: 'black',
  width: '100%',
  height: value > 4 ? `calc(2px + ${value-4}%)` : '2px'
})

interface AnimationPositionI {
  value: number
}

const AnimationPosition: React.FunctionComponent<AnimationPositionI> = ({ value }) => {

  return (
    <div css={componentS}>
      <div css={blindsS(value)}>
        &nbsp;
      </div>
    </div>
  )
}

export default AnimationPosition