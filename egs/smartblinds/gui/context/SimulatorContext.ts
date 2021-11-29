import { createContext } from 'react'
import { DocumentI, FeaturesValuesI } from './DataContext'

export interface SimulatorContextI {
    simFeatureVector: FeaturesValuesI
    setSimFeatureVector: (features: FeaturesValuesI) => void
    updateSimFeatureVector: (featureName: string, value: number | boolean) => void
}

const SimulatorContext = createContext<SimulatorContextI>({} as SimulatorContextI)

export default SimulatorContext