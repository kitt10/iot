import React, { useContext } from 'react'
import { css } from '@emotion/react'
import PageContext from '../context/PageContext'


const componentS = () => css({
  fontSize: '12px',
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'center'
})

const Message: React.FunctionComponent = () => {

  const { message } = useContext(PageContext)

  return (
    <div css={componentS}>
      {message}
    </div>
  )
}

export default Message