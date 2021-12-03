import { useState, useEffect } from 'react'
import { DocumentI, ControlsI, DataContextI } from '../context/DataContext'
import config from '../config'

export const useData = () => {

    const [allDocuments, setAllDocuments] = useState([] as DocumentI[])
    const [documents, setDocuments] = useState([] as DocumentI[])
    const [controls, setControls] = useState({} as ControlsI)
    const [trainBack, setTrainBack] = useState(config.defaultTrainBack)
    const [showBack, setShowBack] = useState(config.defaultShowBack)

    const parseData = async (data: Object[]) => {
        setAllDocuments(data as DocumentI[])
    }

    const limitDocuments = async () => {
        setDocuments(allDocuments.filter(doc => doc.timestamp >= showBack))
    }

    useEffect(() => {
        limitDocuments()
      }, [showBack, allDocuments])

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
