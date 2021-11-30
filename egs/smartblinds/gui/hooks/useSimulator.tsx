import { useState, useContext } from 'react'
import { SimulatorContextI } from '../context/SimulatorContext'
import { DocumentI } from '../context/DataContext'
import TaskContext from '../context/TaskContext'

export const useSimulator = (lastDocument: DocumentI) => {

    const taskContext = useContext(TaskContext)
    const [simFeatureVector, setSimFeatureVector] = useState(lastDocument.features)

    const setSimFeature = async (featureName: string, value: number | boolean) => {
        simFeatureVector[featureName] = value
        setSimFeatureVector(simFeatureVector)
    }

    const updateClassifiers = async () => {
        for (let classifier of taskContext.classifiers) {
            classifier.state.simUpdated = true
            taskContext.setClassifiers([...taskContext.classifiers])
        }
    }

    const setClassifiersNotUpdated = async () => {
        for (let classifier of taskContext.classifiers) {
            classifier.state.simUpdated = false
        }

        updateClassifiers()     // RETHINK - do it like this?
    }

    const simulatorContext: SimulatorContextI = {
        simFeatureVector: simFeatureVector,
        setSimFeature: setSimFeature,
        updateClassifiers: updateClassifiers,
        setClassifiersNotUpdated: setClassifiersNotUpdated
    }

    return simulatorContext
}

export default useSimulator
