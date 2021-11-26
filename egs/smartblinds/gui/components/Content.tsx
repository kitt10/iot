import React from 'react'
import { css, SerializedStyles } from '@emotion/react'


const componentS = () => css({
  flexGrow: 1,
  width: 'calc(100% - 50px)',
  margin: '25px',
  overflow: 'scroll'
})

interface ContentI {
  contentAS?: () => SerializedStyles
}

const Content: React.FunctionComponent<ContentI> = props => {

  return (
    <div css={[componentS, props.contentAS]}>
      {props.children}
    </div>
  )
}

export default Content