import { useState } from 'react'
import { DocumentI, DataContextI } from '../context/DataContext'

export const useData = () => {

    const [documents, setDocuments] = useState([] as DocumentI[])

    const dataContext: DataContextI = {
        documents: documents,
        setDocuments: setDocuments
    }

    return dataContext
}

export default useData
