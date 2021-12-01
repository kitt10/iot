import { useState } from 'react'
import { ClassifierI, FeatureI, TargetI, TaskI, TaskContextI, TaskInfoI } from '../context/TaskContext'

export const useTask = () => {

    const [features, setFeatures] = useState([] as FeatureI[])
    const [targets, setTargets] = useState([] as TargetI[])
    const [classifiers, setClassifiers] = useState([] as ClassifierI[])
    const [taskInfo, setTaskInfo] = useState({} as TaskInfoI)

    const setTask = (task: TaskI) => {
        setFeatures(task.features)
        setTargets(task.targets)
        setClassifiers(task.classifiers)
        setTaskInfo(task.taskInfo)
    }

    const taskContext: TaskContextI = {
        features: features,
        targets: targets,
        classifiers: classifiers,
        taskInfo: taskInfo,
        setTask: setTask,
        setClassifiers: setClassifiers
    }

    return taskContext
}

export default useTask
