import { createContext } from 'react'
import { css, SerializedStyles } from '@emotion/react'

const globalStyle = css`
html {
    background: black;
  }
  body {
    min-width: 100vh;
    min-height: 100vh;
    margin: 0 auto;
    background: #eee;
    font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
    font-size: 15px;
  }

a {
  color: inherit;
  text-decoration: none;
}
`

const pageS = css({
    display: 'flex',
    flexDirection: 'column',
    minWidth: '100vh',
    minHeight: '100vh',
    maxHeight: '100vh',
    overflow: 'hidden'
  })

export interface StyleI {
    globalStyle: SerializedStyles
    pageS: SerializedStyles
}

export interface PageContextI {
    style: StyleI
}

export const defaultPageContext: PageContextI = {
    style: {
        globalStyle: globalStyle,
        pageS: pageS
    }
}

const PageContext = createContext<PageContextI>({} as PageContextI)

export default PageContext
