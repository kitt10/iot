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
    features: FeaturesValuesI
    targets: TargetsValuesI
}

export interface DataContextI {
    documents: DocumentI[]
    parseData: (data: Object[]) => void
}

export interface PayloadControlI {
    status: string
    targets: TargetsValuesI
    controlTime: number
}

export interface PayloadTrainI {
    status: string
    classifierInfo: {
        [classifierName: string]: {
            trainTime: number
            lastTrained: number
            nSamples: number
        }
    }
}

const DataContext = createContext<DataContextI>({} as DataContextI)

export default DataContext