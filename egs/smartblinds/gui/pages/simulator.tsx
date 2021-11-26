import React, { useContext } from 'react'
import { css } from '@emotion/react'
import Page from '../components/core/Page'
import Header from '../components/Header'
import Content from '../components/Content'
import FeatureTuner from '../components/FeatureTuner'
import ClassificationFrame from '../components/ClassificationFrame'

const contentAS = () => css({
  display: 'flex',
  flexDirection: 'row'
})

const SimulatorPage = () => {

  const title: string = 'Smartblinds - Simulator'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'

  return (
    <Page title={title} description={description}>
      <Header titleText={title} currentPage='simulator' />
      <Content contentAS={contentAS}>
        <FeatureTuner />
        <ClassificationFrame />
      </Content>
    </Page>
  )
}

export default SimulatorPage
