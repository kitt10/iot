import { css } from '@emotion/react'
import { SerializedStyles } from '@mui/styled-engine'
import Icon, { IconI } from './Icon'

export const buttonS = () => css({
    textDecoration: 'none',
    cursor: 'pointer',
    border: 'none',
    backgroundColor: 'inherit'
})

export interface ButtonI {
    onClick: () => void
    buttonStyle?: () => SerializedStyles
    title?: string
}

const IconButton: React.FunctionComponent<IconI & ButtonI> = (props) => {
    
    const iconProps: IconI = {
        color: props.color,
        fontSize: props.fontSize,
        iconStyle: props.iconStyle
    }

    const buttonProps = {
        onClick: props.onClick,
        title: props.title
    }

    return (
        <button css={[buttonS, props.buttonStyle]} {...buttonProps}>
            <Icon {...iconProps}>{props.children}</Icon>
        </button>
    )
}

export default IconButton
