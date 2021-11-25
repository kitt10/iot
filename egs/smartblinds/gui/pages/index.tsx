import { useEffect } from 'react'
import { css } from '@emotion/react'
import { useState } from 'react'
import Page from '../components/core/Page'
import { useRouter } from 'next/router'
import Header from '../components/Header'
import Content from '../components/Content'

const blindsS = (countDown: number, animationTime: number) => css({
  width: '100%',
  flex: countDown/animationTime * 10,
  margin: '0 auto',
  backgroundColor: 'darkgray',
  borderBottom: '1px solid black'
})

const IndexPage = () => {

  const title: string = 'Smartblinds'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'

  const animationTime: number = 2000    // [ms]
  const step: number = 10              // [ms]

  const router = useRouter()
  const [countDown, setCountDown] = useState(animationTime)

  const redirect = () => {
    router.push('/live')
  }

  useEffect(() => {
    /** Make the animation and then redirect to the /live page in 2 secs after load. */
    if (countDown > 0) {
      setTimeout(() => {setCountDown(countDown-step)}, step)
    } else {
      redirect()
    }
  }, [countDown])

  return (
    <Page title={title} description={description}>
      <Header titleText={title} currentPage='index' />
      <Content>
        <div css={blindsS(countDown, animationTime)}>
          &nbsp;
        </div>
        <div css={{'flex': (10 - countDown/animationTime * 10)}}>
          &nbsp;
        </div>
      </Content>
    </Page>
  )
}

export default IndexPage
