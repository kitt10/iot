import React from 'react'
import { css } from '@emotion/react'


const componentS = () => css({
  flexGrow: 1,
  width: 'calc(100% - 50px)',
  margin: '25px',
  border: '1px solid green'
})

const Content: React.FunctionComponent = props => {

  return (
    <div css={componentS}>
      {props.children}
    </div>
  )
}

export default Content