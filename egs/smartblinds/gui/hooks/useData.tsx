import { useState } from 'react'
import { DocumentI, DataContextI } from '../context/DataContext'

export const useData = () => {

    const [documents, setDocuments] = useState([] as DocumentI[])

    const parseData = async (data: Object[]) => {
        const docs: DocumentI[] = data as DocumentI[]
        setDocuments(docs)
    }

    const dataContext: DataContextI = {
        documents: documents,
        parseData: parseData
    }

    return dataContext
}

export default useData
