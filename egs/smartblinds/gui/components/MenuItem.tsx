import React from 'react'
import { css } from '@emotion/react'
import Link from 'next/link'

const componentS = (isSelected: boolean) => css({
  marginLeft: '25px',
  color: isSelected ? 'darkblue' : 'inherit',
  textDecoration: isSelected ? 'underline' : 'none'
})

export interface MenuItemI {
    text: string
    href: string
    isSelected: boolean
}

const MenuItem: React.FunctionComponent<MenuItemI> = props => {

  return (
    <div css={componentS(props.isSelected)}>
      <Link href={props.href}>
        {props.text}
      </Link>
    </div>
  )
}

export default MenuItem