import React from 'react'
import { css } from '@emotion/react'
import MenuItem from './MenuItem'

const componentS = () => css({
  marginRight: '25px',
  marginTop: '25px',
  fontSize: '25px',
  display: 'flex',
  flexDirection: 'row-reverse',
  width: '25%'         // to make the message centered
})

export interface MenuI {
    currentPage: string
}

const Menu: React.FunctionComponent<MenuI> = ({ currentPage }) => {

  return (
    <div css={componentS}>
      <MenuItem text='Live' href='/live' isSelected={currentPage == 'live'} />
      <MenuItem text='Simulator' href='/simulator' isSelected={currentPage == 'simulator'} />
      <MenuItem text='Data' href='/data' isSelected={currentPage == 'data'} />
      <MenuItem text='Control' href='/control' isSelected={currentPage == 'control'} />
    </div>
  )
}

export default Menu