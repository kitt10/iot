import React from 'react'
import { css } from '@emotion/react'
import Link from 'next/link'


const componentS = () => css({
  marginLeft: '25px',
  marginTop: '25px',
  fontSize: '25px',
  fontWeight: 'bold',
  width: '35%'         // to make the message centered
})

export interface TitleI {
    titleText: string
}

const Title: React.FunctionComponent<TitleI> = ({ titleText }) => {

  return (
    <div css={componentS}>
      <Link href='/'>
        {titleText}
      </Link>
    </div>
  )
}

export default Title