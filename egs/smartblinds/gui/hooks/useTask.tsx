import { useState } from 'react'
import { FeatureI, TargetI, TaskContextI } from '../context/TaskContext'

export const useTask = () => {

    const [features, setFeatures] = useState([] as FeatureI[])
    const [targets, setTargets] = useState([] as TargetI[])

    const setTask = (features: FeatureI[], targets: TargetI[]) => {
        setFeatures(features)
        setTargets(targets)
    }

    const taskContext: TaskContextI = {
        features: features,
        targets: targets,
        setTask: setTask
    }

    return taskContext
}

export default useTask
