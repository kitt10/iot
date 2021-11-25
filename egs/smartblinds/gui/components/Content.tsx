import React from 'react'
import { css } from '@emotion/react'


const componentS = () => css({
  flexGrow: 1,
  width: 'calc(100% - 50px)',
  margin: '25px',
  display: 'flex',
  flexDirection: 'column'
})

const Content: React.FunctionComponent = props => {

  return (
    <div css={componentS}>
      {props.children}
    </div>
  )
}

export default Content