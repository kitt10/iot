import type { AppProps } from 'next/app'
import { Global } from '@emotion/react'
import PageContext from '../context/PageContext'
import { usePage } from '../hooks/usePage'

const MainApp = ({ Component, pageProps }: AppProps) => {

  const pageContext = usePage()

  return (
    <PageContext.Provider value={pageContext}>
      <Global styles={pageContext.style.globalStyle} />
      <Component {...pageProps} />
    </PageContext.Provider>
  )
}

export default MainApp
