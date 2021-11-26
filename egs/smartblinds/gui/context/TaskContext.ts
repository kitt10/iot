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

export interface TaskI {
    features: FeatureI[]
    targets: TargetI[]
}

export interface TaskContextI extends TaskI {
    setTask: (features: FeatureI[], targets: TargetI[]) => void
}

const TaskContext = createContext<TaskContextI>({} as TaskContextI)

export default TaskContext