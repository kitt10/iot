import { css } from '@emotion/react'
import { SerializedStyles } from '@mui/styled-engine'

export const inputS = () => css({
    backgroundColor: 'inherit',
    border: '1px solid black'
})

export interface InputI {
    inputRef?: React.RefObject<HTMLInputElement>
    inputStyle?: () => SerializedStyles
}

const Icon: React.FunctionComponent<InputI & React.HTMLProps<HTMLInputElement>> = ({ inputRef, inputStyle, ...otherProps }) => {

    return (
        <input ref={inputRef} css={[inputS, inputStyle]} {...otherProps} />
    )
}

export default Icon
