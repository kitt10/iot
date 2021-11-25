import React, { useContext, useEffect } from 'react'
import { css } from '@emotion/react'
import PageContext from '../context/PageContext'
import Page from '../components/core/Page'
import Header from '../components/Header'
import Content from '../components/Content'

const SimulatorPage = () => {

  const title: string = 'Smartblinds - Simulator'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'


  return (
    <Page title={title} description={description}>
      <Header titleText={title} currentPage='simulator' />
      <Content>
        {'content simulator page'}
      </Content>
    </Page>
  )
}

export default SimulatorPage
