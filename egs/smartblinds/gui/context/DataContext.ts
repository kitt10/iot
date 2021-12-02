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

export interface ControlsI {
    [classifierName: string]: {
        controlByTs: {
            [timestamp: number]: {
                position: number
                tilt: number
            }
        }
        tsMin: number
        tsMax: number
    }
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

export interface DataContextI {
    documents: DocumentI[]
    controls: ControlsI
    setControls: (controls: ControlsI) => void
    trainBack: number
    setTrainBack: (trainBack: number) => void
    showBack: number
    setShowBack: (showBack: number) => void
    parseData: (data: Object[]) => void
}

const DataContext = createContext<DataContextI>({} as DataContextI)

export default DataContext