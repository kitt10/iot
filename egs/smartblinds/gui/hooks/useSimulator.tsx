import { useState } from 'react'
import { SimulatorContextI, ClassifiersUpdatedI } from '../context/SimulatorContext'
import { DocumentI } from '../context/DataContext'

export const useSimulator = (lastDocument: DocumentI, classifiersNames: string[]) => {

    const [simFeatureVector, setSimFeatureVector] = useState(lastDocument.features)
    const defaultClassifiersUpdated: ClassifiersUpdatedI = Object.assign({}, ...classifiersNames.map((name: string) => ({[name]: false})))
    const [classifiersUpdated, setClassifiersUpdated] = useState(defaultClassifiersUpdated)

    const setSimFeature = async (featureName: string, value: number | boolean) => {
        simFeatureVector[featureName] = value
        setSimFeatureVector(simFeatureVector)
    }

    const setClassifierUpdated = async (classifierName: string, value: boolean) => {
        classifiersUpdated[classifierName] = value
        setClassifiersUpdated(classifiersUpdated)
    }

    const simulatorContext: SimulatorContextI = {
        simFeatureVector: simFeatureVector,
        setSimFeature: setSimFeature,
        classifiersUpdated: classifiersUpdated,
        setClassifierUpdated: setClassifierUpdated
    }

    return simulatorContext
}

export default useSimulator
