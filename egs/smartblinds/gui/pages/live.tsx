import Page from '../components/core/Page'
import Header from '../components/Header'
import Content from '../components/Content'
import InfoBar from '../components/InfoBar'

const LivePage = () => {

  const title: string = 'Smartblinds - Live Control'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'

  return (
    <Page title={title} description={description}>
      <Header titleText={title} currentPage='live' />
      <Content>
        {'content live page'}
      </Content>
      <InfoBar />
    </Page>
  )
}

export default LivePage
