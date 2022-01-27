import { useState, useContext, useCallback, useEffect } from 'react'
import { ControlContextI } from '../context/ControlContext'
import { TargetsValuesI, PayloadControlI } from '../context/DataContext'
import TaskContext from '../context/TaskContext'
import { control } from '../fcn/clientSide'
import config from '../config'

export const useControl = (targetsValues: TargetsValuesI) => {

    const [targetVector, setTargetVector] = useState(targetsValues);
    const [targetNew, setTargetNew] = useState(targetsValues)
    const [preview, setPreview] = useState<boolean>(false);
    const [loading, setLoading] = useState<boolean>(false);
    const [testMode, setTestMode] = useState<boolean>(true);
    const [wsState, setWsState] = useState<number>(3);
    
    const isBrowser = typeof window !== "undefined";

    const [ws, setWs] = useState<WebSocket|null>(null);

    const reconnect = () => {
        if(!isBrowser) return setWs(null);
        if(ws!=null){
            var wsStatus = ws?.readyState;
            if(wsStatus !== 3)
                ws.close();
                setWsState(ws?.readyState)
            if(wsStatus == 3){
                const newWs = new WebSocket(config.ep_ws);
                setWs(newWs);
                setWsState(ws?.readyState)
            }
        }
    }


    // (Optional) Open a connection on mount
    useEffect(() => {
        if(isBrowser) { 
            const ws = new WebSocket(config.ep_ws)
            setWs(ws);
        }

        return () => {
        // Cleanup on unmount if ws wasn't closed already
        if(ws!=null && ws?.readyState !== 3) 
            ws.close()
        }
    }, [])

    if(ws!=null){
        ws.onopen = (ev) => {
            console.log("WS client: Websocket opened.");
            setWsState(ws?.readyState)
        }
        ws.onmessage = (ev) => {
            var d = new Date();
            var data;
            try {
                data = JSON.parse(ev.data);
                if(data.hasOwnProperty("position")){
                    setCurrentTarget('position', data.position);
                }
                if(data.hasOwnProperty("tilt")){
                    setCurrentTarget('tilt', data.tilt);
                }
                if(data.hasOwnProperty("testing")){
                    setTestMode(data.testing);
                }
            } catch(e) {
                data = ev.data;
            }
            console.log(d.toLocaleTimeString(), "WS message:", data);
            setLoading(false);
        }
        ws.onclose = (ev) => {
            setWsState(ws?.readyState)
        }
    }

    const setCurrentTarget = async (targetName: string, value: number) => {
        targetVector[targetName] = value
        setTargetVector({...targetVector})
    }

    const setNewTarget = async (targetName: string, value: number) => {
        targetNew[targetName] = value
        setTargetNew({...targetNew})
    }

    const updateBlindState = async (targetName: string) => {
        let msg = {[targetName]: targetNew[targetName]}
        setLoading(true);
        setPreview(false);
        ws?.send(JSON.stringify(msg))
    }

    const updateTestMode = async (value:boolean) => {
        ws?.send(JSON.stringify({testing: value}))
    }

    const controlContext: ControlContextI = {
        ws: ws,
        wsState: wsState,
        targetVector: targetVector,
        targetNew: targetNew,
        preview: preview,
        loading: loading,
        testMode: testMode,
        reconnectWS: reconnect,
        setCurrentTarget: setCurrentTarget,
        updateBlindState: updateBlindState,
        setNewTarget: setNewTarget,
        setPreview: setPreview,
        setLoading: setLoading,
        setTestMode: updateTestMode
    }

    return controlContext
}

export default useControl
