import { css } from '@emotion/react'
import LiveContext, { LiveContextI } from '../context/LiveContext'
import useLive from '../hooks/useLive'
import Page from '../components/core/Page'
import Header from '../components/Header'
import Content from '../components/Content'
import InfoBar from '../components/InfoBar'
import LiveSamples from '../components/LiveSamples'

const contentAS = () => css({
  display: 'flex',
  flexDirection: 'row'
})

const LivePage = () => {

  const title: string = 'Smartblinds - Live'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'

  const liveContext: LiveContextI = useLive()

  return (
    <Page title={title} description={description}>
      <Header titleText={title} currentPage='live' />
      <Content contentAS={contentAS}>
        <LiveContext.Provider value={liveContext}>
          <LiveSamples /> 
        </LiveContext.Provider>
      </Content>
      <InfoBar />
    </Page>
  )
}

export default LivePage
