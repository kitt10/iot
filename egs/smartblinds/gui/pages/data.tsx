import { css } from '@emotion/react'
import Page from '../components/core/Page'
import Header from '../components/Header'
import Content from '../components/Content'
import DataTable from '../components/DataTable'
import DataLegend from '../components/DataLegend'
import InfoBar from '../components/InfoBar'

const contentAS = () => css({
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'start'
})

const DataPage = () => {

  const title: string = 'Smartblinds - Data'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'

  return (
    <Page title={title} description={description}>
      <Header titleText={title} currentPage='data' />
      <Content contentAS={contentAS}>
        <DataTable />
        <DataLegend />
      </Content>
      <InfoBar />
    </Page>
  )
}

export default DataPage
