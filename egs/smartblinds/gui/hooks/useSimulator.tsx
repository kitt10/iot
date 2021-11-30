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
        /** Set all not updated */
        for (let classifier of taskContext.classifiers) {
            classifier.state.sim.updated = false
        }

        /** Update all one by one */
        for (let classifier of taskContext.classifiers) {
            classifier.state.sim.updated = true
            taskContext.setClassifiers([...taskContext.classifiers])
        }
    }

    const simulatorContext: SimulatorContextI = {
        simFeatureVector: simFeatureVector,
        setSimFeature: setSimFeature,
        updateClassifiers: updateClassifiers
    }

    return simulatorContext
}

export default useSimulator
