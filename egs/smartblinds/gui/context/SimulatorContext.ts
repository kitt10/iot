import { createContext } from 'react'
import { FeaturesValuesI } from './DataContext'

export interface SimulatorContextI {
    simFeatureVector: FeaturesValuesI
    setSimFeature: (featureName: string, value: number | boolean) => void
    updateClassifiers: () => void
}

const SimulatorContext = createContext<SimulatorContextI>({} as SimulatorContextI)

export default SimulatorContext