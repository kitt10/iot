import React, { useContext, useEffect } from 'react'
import { css } from '@emotion/react'
import PageContext from '../context/PageContext'
import Page from '../components/core/Page'
import Header from '../components/Header'
import Content from '../components/Content'

const DataPage = () => {

  const title: string = 'Smartblinds - Data'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'

  const { planMessage } = useContext(PageContext)

  useEffect(() => {
    const plannedMessage = {newMessage: 'Loading data...', lasting: 2000}
    planMessage(plannedMessage)
  }, [])

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