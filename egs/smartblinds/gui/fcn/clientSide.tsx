import { post } from './httpFetch'
import config from '../config'
import { FeaturesValuesI, PayloadControlI, PayloadPredictI, PayloadTrainI } from '../context/DataContext'

export const control = async (classifier_name: string, features: FeaturesValuesI) => {
    let payload: PayloadControlI = {} as PayloadControlI
    await post(config.ep_control, null, {classifier_name: classifier_name, features: features})
        .then(reply => {
            if (reply.payload.status == 'ok') {
                payload = reply.payload
            } else {
                console.log('ERROR: Bad status in control:', classifier_name, reply.payload.status)
            }
        })
        .catch(err => {
            console.log('ERROR in control:', classifier_name, err)
        })
    return payload
}

export const predict = async (classifiers: string[], ts_start: number, signal: AbortSignal) => {
    let payload: PayloadPredictI = {} as PayloadPredictI
    await post(config.ep_predict, signal, {classifiers: classifiers, ts_start: ts_start})
        .then(reply => {
            if (reply.payload.status == 'ok') {
                payload = reply.payload
            } else {
                console.log('ERROR: Bad status in predict:', reply.payload.status)
            }
        })
        .catch(err => {
            console.log('ERROR in predict:', err)
            if(err.name === 'AbortError'){
                throw(err)
            }
        })
    return payload
}

export const trainAll = async () => {
    let payload: PayloadTrainI = {} as PayloadTrainI
    await post(config.ep_train, null, {})
        .then(reply => {
            if (reply.payload.status == 'ok') {
                payload = reply.payload
            } else {
                console.log('ERROR: Bad status in train:', reply.payload.status)
            }
        })
        .catch(err => {
            console.log('ERROR in train:', err)
        })
    return payload.classifierInfo
}