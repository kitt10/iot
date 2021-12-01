import { post } from './httpFetch'
import config from '../config'
import { FeaturesValuesI, PayloadControlI, PayloadTrainI } from '../context/DataContext'

export const control = async (classifier_name: string, features: FeaturesValuesI) => {
    let payload: PayloadControlI = {} as PayloadControlI
    await post(config.ep_control, {classifier_name: classifier_name, features: features})
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

export const trainAll = async () => {
    let payload: PayloadTrainI = {} as PayloadTrainI
    await post(config.ep_train, {})
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