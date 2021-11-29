import { useState } from 'react'
import { SimulatorContextI } from '../context/SimulatorContext'
import { DocumentI } from '../context/DataContext'

export const useSimulator = (lastDocument: DocumentI) => {

    const [simFeatureVector, setSimFeatureVector] = useState(lastDocument.features)

    const updateSimFeatureVector = async (featureName: string, value: number | boolean) => {
        simFeatureVector[featureName] = value
        setSimFeatureVector(simFeatureVector)
    }

    const simulatorContext: SimulatorContextI = {
        simFeatureVector: simFeatureVector,
        setSimFeatureVector: setSimFeatureVector,
        updateSimFeatureVector: updateSimFeatureVector
    }

    return simulatorContext
}

export default useSimulator
