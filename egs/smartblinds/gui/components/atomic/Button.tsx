import { css } from '@emotion/react'
import { SerializedStyles } from '@mui/styled-engine'

export const buttonS = () => css({
    textDecoration: 'none',
    cursor: 'pointer',
    border: 'none',
    backgroundColor: 'inherit'
})

export interface ButtonI {
    text: string
    onClick: () => void
    buttonStyle?: () => SerializedStyles
    title?: string
}

const Button: React.FunctionComponent<ButtonI> = (props) => {

    const buttonProps = {
        onClick: props.onClick,
        title: props.title
    }

    return (
        <button css={[buttonS, props.buttonStyle]} {...buttonProps}>
            {props.text}
        </button>
    )
}

export default Button
