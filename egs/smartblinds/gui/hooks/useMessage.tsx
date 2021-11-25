import { useState } from 'react'
import { plannedMessageI } from '../context/PageContext'

export const useMessage = () => {

    const [message, setMessage] = useState('')
    const [plannedMessages, setPlannedMessages] = useState([] as plannedMessageI[])

    const putMessage = (plannedMessage: plannedMessageI) => {
        setMessage(plannedMessage.newMessage)
        setTimeout(clearMessage, plannedMessage.lasting)
    }

    const clearMessage = () => {
        plannedMessages.shift()
        setPlannedMessages(plannedMessages)
        if (plannedMessages.length > 0) {
            putMessage(plannedMessages[0])
        } else {
            setMessage('')
        }
    }

    const planMessage = async (plannedMessage: plannedMessageI) => {
        plannedMessages.push(plannedMessage)
        setPlannedMessages(plannedMessages)
        if (message == '') {
            putMessage(plannedMessages[0])
        }
    }

    return {message: message, planMessage: planMessage}
}

export default useMessage
