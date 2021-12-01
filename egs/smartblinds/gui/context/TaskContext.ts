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
    trainable: boolean
    nSamples: number
    retrained: number
    trainTime: number
    controlTime: number
    state: {
        sim: {
            updated: boolean
            position: number
            tilt: number
        }
    }
}

export const defaultClassifierState = {
    sim: {
        updated: false,
        position: 0,
        tilt: 0
    }
}

export interface TaskI {
    features: FeatureI[]
    targets: TargetI[]
    classifiers: ClassifierI[]
}

export interface TaskContextI extends TaskI {
    setTask: (task: TaskI) => void
    setClassifiers: (classifiers: ClassifierI[]) => void
}

const TaskContext = createContext<TaskContextI>({} as TaskContextI)

export default TaskContext