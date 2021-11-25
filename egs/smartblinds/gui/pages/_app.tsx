import type { AppProps } from 'next/app'
import { Global } from '@emotion/react'
import PageContext, { defaultPageContext } from '../context/PageContext'

const MainApp = ({ Component, pageProps }: AppProps) => {

  return (
    <PageContext.Provider value={defaultPageContext}>
      <Global styles={defaultPageContext.style.globalStyle} />
      <Component {...pageProps} />
    </PageContext.Provider>
  )
}

export default MainApp
