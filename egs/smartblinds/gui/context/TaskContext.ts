import { createContext } from 'react'

export interface FeatureI {
    name: string
    type: string
    min: number | undefined
    max: number | undefined
    description: string
}

export interface TargetI {
    name: string
    type: string
    min: number | undefined
    max: number | undefined
    description: string
}

export interface ClassifierI {
    name: string
    description: string
    dataTraining: string[]
}

export interface TaskI {
    features: FeatureI[]
    targets: TargetI[]
    classifiers: ClassifierI[]
}

export interface TaskContextI extends TaskI {
    setTask: (task: TaskI) => void
}

const TaskContext = createContext<TaskContextI>({} as TaskContextI)

export default TaskContext