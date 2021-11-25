import { useEffect } from 'react'
import Page from '../components/core/Page'
import { useRouter } from 'next/router'
import Header from '../components/Header'
import Content from '../components/Content'

const IndexPage = () => {

  const title: string = 'Smartblinds'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'

  const router = useRouter()

  const redirect = () => {
    router.push('/live')
  }

  useEffect(() => {
    /** Redirect to the /live page in 2 secs after load. */
    setTimeout(redirect, 2000)
  }, [])

  return (
    <Page title={title} description={description}>
      <Header titleText={title} currentPage='index' />
      <Content>
        {'content index page'}
      </Content>
    </Page>
  )
}

export default IndexPage
