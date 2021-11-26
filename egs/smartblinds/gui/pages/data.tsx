import React from 'react'
import Page from '../components/core/Page'
import Header from '../components/Header'
import Content from '../components/Content'

const DataPage = () => {

  const title: string = 'Smartblinds - Data'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'

  return (
    <Page title={title} description={description}>
      <Header titleText={title} currentPage='data' />
      <Content>
        {'content data page'}
      </Content>
    </Page>
  )
}

export default DataPage
