import { useState } from 'react'
import { globalStyle, pageS, PageContextI, plannedMessageI } from '../context/PageContext'

export const usePage = () => {

    const [message, setMessage] = useState('')
    const plannedMessages = [] as plannedMessageI[]

    const popUpMessage = (message: string) => {
        //setInfoMessage(message)
        setTimeout(clearMessage, 2000)
    }

    const clearMessage = () => {
        //setInfoMessage('')
    }

    const planMessage = (props: plannedMessageI) => {
        plannedMessages.push(props)
    }

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
