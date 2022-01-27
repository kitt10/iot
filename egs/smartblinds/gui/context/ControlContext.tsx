import { createContext } from 'react'
import { TargetsValuesI } from './DataContext'

export interface ControlContextI {
    ws: WebSocket|null
    wsState: number|null
    targetVector: TargetsValuesI
    targetNew: TargetsValuesI
    preview: boolean
    loading: boolean
    testMode: boolean
    reconnectWS: () => void
    setCurrentTarget: (targetName: string, value: number) => void
    setNewTarget: (targetName: string, value: number) => void
    updateBlindState: (targetName: string) => void
    setPreview: (value: boolean) => void
    setLoading: (value: boolean) => void
    setTestMode: (value: boolean) => void
}

const ControlContext = createContext<ControlContextI>({} as ControlContextI)

export default ControlContext