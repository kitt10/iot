import React from 'react'
import { css } from '@emotion/react'


const componentS = () => css({
  fontSize: '12px',
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'center'
})

const Message: React.FunctionComponent = () => {

  const message: string = 'message'

  return (
    <div css={componentS}>
      {message}
    </div>
  )
}

export default Message