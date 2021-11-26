import { createContext } from 'react'

export interface FeaturesValuesI {
    [feature_name: string]: number | boolean
}

export interface TargetsValuesI {
    [target_name: string]: number
}

export interface DocumentI {
    timestamp: number
    testing: boolean
    periodical: boolean
    featureValue: FeaturesValuesI
    targetValue: TargetsValuesI
}

export interface DataContextI {
    documents: DocumentI[]
    parseData: (data: Object[]) => void
}

const DataContext = createContext<DataContextI>({} as DataContextI)

export default DataContext