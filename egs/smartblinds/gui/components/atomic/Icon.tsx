import { css } from '@emotion/react'
import { Icon as DefaultIcon } from '@mui/material'
import { SerializedStyles } from '@mui/styled-engine'

export const iconS = (color?: string, fontSize?: string) => css({
    color: color || 'inherit',
    fontSize: fontSize+' !important'
})

export interface IconI {
    color?: string
    fontSize?: string
    iconStyle?: () => SerializedStyles
}

const Icon: React.FunctionComponent<IconI> = ({ color, fontSize, iconStyle, children }) => {

    return (
        <DefaultIcon css={[iconS(color, fontSize), iconStyle]}>{children}</DefaultIcon>
    )
}

export default Icon
