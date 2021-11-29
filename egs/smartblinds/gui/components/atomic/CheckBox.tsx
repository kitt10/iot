import { css } from '@emotion/react'
import { SerializedStyles } from '@mui/styled-engine'

export const switchS = () => css({
    display: 'flex',
    flexDirection: 'row'
})

export const checkboxS = () => css({
    backgroundColor: 'inherit',
    border: '1px solid black'
})

export const labelS = () => css({
    width: '100%'
})

export interface CheckBoxI {
    labelText: string
    checkboxRef?: React.RefObject<HTMLInputElement>
    switchStyle?: () => SerializedStyles
    checkboxStyle?: () => SerializedStyles
    labelStyle?: () => SerializedStyles
}

const CheckBox: React.FunctionComponent<CheckBoxI & React.HTMLProps<HTMLInputElement>> = ({ labelText, checkboxRef, switchStyle, checkboxStyle, labelStyle, ...otherProps }) => {

    return (
        <label css={[switchS, switchStyle]}>
            <input type="checkbox" ref={checkboxRef} css={[checkboxS, checkboxStyle]} {...otherProps} />
            <span css={[labelS, labelStyle]}>{labelText}</span>
        </label>
    )
}

export default CheckBox
