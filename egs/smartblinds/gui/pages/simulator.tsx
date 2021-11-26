import React, { useContext } from 'react'
import { css } from '@emotion/react'
import Page from '../components/core/Page'
import Header from '../components/Header'
import Content from '../components/Content'
import TaskContext from '../context/TaskContext'

const SimulatorPage = () => {

  const title: string = 'Smartblinds - Simulator'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'

  const { features, targets } = useContext(TaskContext)
  console.log('features:', features)

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
