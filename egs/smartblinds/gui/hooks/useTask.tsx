import { useState } from 'react'
import { ClassifierI, FeatureI, TargetI, TaskI, TaskContextI } from '../context/TaskContext'

export const useTask = () => {

    const [features, setFeatures] = useState([] as FeatureI[])
    const [targets, setTargets] = useState([] as TargetI[])
    const [classifiers, setClassifiers] = useState([] as ClassifierI[])

    const setTask = (task: TaskI) => {
        setFeatures(task.features)
        setTargets(task.targets)
        setClassifiers(task.classifiers)
    }

    const taskContext: TaskContextI = {
        features: features,
        targets: targets,
        classifiers: classifiers,
        setTask: setTask
    }

    return taskContext
}

export default useTask
