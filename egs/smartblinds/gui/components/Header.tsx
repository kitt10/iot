import React from 'react'
import { css } from '@emotion/react'
import Title from '../components/Title'
import Menu from '../components/Menu'
import Message from './Message'


const componentS = () => css({
  flexGrow: 0,
  width: '100%',
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'space-between'
})

export interface HeaderI {
  titleText: string
  currentPage: string
}

const Header: React.FunctionComponent<HeaderI> = ({ titleText, currentPage }) => {

  return (
    <div css={componentS}>
      <Title titleText={titleText} />
      <Message />
      <Menu currentPage={currentPage} />
    </div>
  )
}

export default Header