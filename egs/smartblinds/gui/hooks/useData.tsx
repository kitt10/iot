import { useState } from 'react'
import { DocumentI, ControlsI, DataContextI } from '../context/DataContext'
import config from '../config'

export const useData = () => {

    const [documents, setDocuments] = useState([] as DocumentI[])
    const [controls, setControls] = useState({} as ControlsI)
    const [trainBack, setTrainBack] = useState(config.defaultTrainBack)
    const [showBack, setShowBack] = useState(config.defaultShowBack)

    const parseData = async (data: Object[]) => {
        const docs: DocumentI[] = data as DocumentI[]
        setDocuments(docs)
    }

    const dataContext: DataContextI = {
        documents: documents,
        parseData: parseData,
        trainBack: trainBack,
        setTrainBack: setTrainBack,
        showBack: showBack,
        setShowBack: setShowBack,
        controls: controls,
        setControls: setControls
    }

    return dataContext
}

export default useData
