import { createContext } from 'react'
import { FeaturesValuesI } from './DataContext'

export interface ClassifiersUpdatedI {
    [classifierName: string]: boolean
}

export interface SimulatorContextI {
    simFeatureVector: FeaturesValuesI
    setSimFeature: (featureName: string, value: number | boolean) => void
    classifiersUpdated: ClassifiersUpdatedI
    setClassifierUpdated: (classifierName: string, value: boolean) => void
}

const SimulatorContext = createContext<SimulatorContextI>({} as SimulatorContextI)

export default SimulatorContext