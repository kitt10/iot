import { createContext } from 'react'

export interface DocumentI {
    [feature_or_target: string]: string | number | boolean
}

export interface DataContextI {
    documents: DocumentI[]
    setDocuments: (documents: DocumentI[]) => void
}

const DataContext = createContext<DataContextI>({} as DataContextI)

export default DataContext