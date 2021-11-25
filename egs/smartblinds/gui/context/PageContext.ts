import { createContext } from 'react'
import { css, SerializedStyles } from '@emotion/react'

export const globalStyle = css`
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

export const pageS = css({
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

export interface plannedMessageI {
  newMessage: string
  lasting: number         // [ms]
}

export interface PageContextI {
    style: StyleI
    message: string
    planMessage: (plannedMessage: plannedMessageI) => void
}

const PageContext = createContext<PageContextI>({} as PageContextI)

export default PageContext
