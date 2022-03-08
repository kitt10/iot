import { useState, useEffect } from 'react'
import { DocumentI, ControlsI, DataContextI, PredictionI, PredictionsI, PayloadPredictI } from '../context/DataContext'
import config from '../config'
import { post } from '../fcn/httpFetch'

export const useData = () => {

    const [allDocuments, setAllDocuments] = useState([] as DocumentI[])
    const [documents, setDocuments] = useState([] as DocumentI[])
    const [controls, setControls] = useState({} as ControlsI)
    const [predictions, setPredictions] = useState({} as PredictionsI)
    const [trainBack, setTrainBack] = useState(config.defaultTrainBack)
    const [showBack, setShowBack] = useState(config.defaultShowBack)

    const parseData = async (data: Object[]) => {
        setAllDocuments(data as DocumentI[])
    }

    const limitDocuments = async () => {
        setDocuments(allDocuments.filter(doc => doc.timestamp >= showBack))
    }

    useEffect(() => {
        limitDocuments()
      }, [showBack, allDocuments])

    useEffect(() => {
        getPredictions()
      }, [showBack])

    const getPredictions = () => {
        let predictions = {status: "bad"} as PayloadPredictI
        post(config.ep_predict, null, {ts_start: showBack, classifiers: ["ifelse"]}).then(payload => {
            predictions = payload.payload;
            setPredictions(predictions);
            console.log(predictions)})
      }

    const dataContext: DataContextI = {
        documents: documents,
        parseData: parseData,
        trainBack: trainBack,
        setTrainBack: setTrainBack,
        showBack: showBack,
        setShowBack: setShowBack,
        controls: controls,
        setControls: setControls,
        predictions: predictions,
        setPredictions: setPredictions
    }

    return dataContext
}

export default useData
