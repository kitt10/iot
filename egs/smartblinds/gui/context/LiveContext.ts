import { createContext } from 'react'
import { DocumentI } from './DataContext'
import { FeatureI } from './TaskContext'

export interface LiveContextI {
    samplesTitle: string
    updateSamplesTitle: (document: DocumentI, feature: FeatureI) => void
    setSamplesTitle: (newTitle: string) => void
}

const LiveContext = createContext<LiveContextI>({} as LiveContextI)

export default LiveContext