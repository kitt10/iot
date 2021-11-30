import { post } from './httpFetch'
import config from '../config'
import { FeaturesValuesI, TargetsValuesI } from '../context/DataContext'

export const control = async (classifier_name: string, features: FeaturesValuesI) => {
    let targets: TargetsValuesI = {}
    await post(config.ep_control, {classifier_name: classifier_name, features: features})
        .then(payload => {
            targets = payload.data
        })
        .catch(err => {
            console.log('ERROR in control:', classifier_name, err)
        })
    return targets
}