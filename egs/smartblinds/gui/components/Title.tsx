import React, { useContext } from 'react'
import { css } from '@emotion/react'
import Link from 'next/link'
import PageContext from '../context/PageContext'
import Message from './Message'

const componentS = () => css({
  marginLeft: '25px',
  marginTop: '25px',
  fontSize: '25px',
  fontWeight: 'bold',
  width: '25%'         // to make the middle component centered
})

export interface TitleI {
    titleText: string
}

const Title: React.FunctionComponent<TitleI> = ({ titleText }) => {

  const { message } = useContext(PageContext)

  return (
    <div css={componentS}>
      {message != '' && <Message />}
      {message == '' && <Link href='/'>
        {titleText}
      </Link>}
    </div>
  )
}

export default Title