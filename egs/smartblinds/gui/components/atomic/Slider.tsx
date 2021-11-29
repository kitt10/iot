import { css } from '@emotion/react'
import { SerializedStyles } from '@mui/styled-engine'

export const sliderS = () => css({
    backgroundColor: 'inherit',
    border: '1px solid black'
})

export const containerS = () => css({
    width: '100%'
})

export interface SliderI {
    sliderRef?: React.RefObject<HTMLInputElement>
    sliderStyle?: () => SerializedStyles
    containerStyle?: () => SerializedStyles
}

const Slider: React.FunctionComponent<SliderI & React.HTMLProps<HTMLInputElement>> = ({ sliderRef, sliderStyle, containerStyle, ...otherProps }) => {

    return (
        <div css={[containerS, containerStyle]}>
            <input type="range" ref={sliderRef} css={[sliderS, sliderStyle]} {...otherProps} />
        </div>
    )
}

export default Slider
