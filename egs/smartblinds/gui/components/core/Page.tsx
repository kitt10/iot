import type { NextPage } from 'next'
import Head from 'next/head'
import React, { useContext } from 'react'
import PageContext from '../../context/PageContext'

export interface PageI {
    title: string
    description: string
}

const Page: NextPage<PageI> = props => {
    const { style } = useContext(PageContext)

    return (
      <div css={style.pageS}>
        <Head>
            <title>{props.title}</title>
            <meta name="description" content={props.description} />
            <link rel="icon" href="/favicon.ico" />
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet"></link>
        </Head>
        {props.children}
      </div>
    )
  }
  
  export default Page