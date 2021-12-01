import { post } from './httpFetch'
import config from '../config'
import { FeaturesValuesI, PayloadControlI } from '../context/DataContext'

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