import { globalStyle, pageS, PageContextI } from '../context/PageContext'
import useMessage from './useMessage'

export const usePage = () => {

    const { message, planMessage } = useMessage()

    const pageContext: PageContextI = {
        style: {
            globalStyle: globalStyle,
            pageS: pageS
        },
        message: message,
        planMessage: planMessage
    }

    return pageContext
}

export default usePage
