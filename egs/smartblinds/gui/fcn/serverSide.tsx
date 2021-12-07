import { load } from 'js-yaml'
import fs from 'promise-fs'
import { post } from './httpFetch'
import { TaskI, defaultClassifierState } from '../context/TaskContext'
import config from '../config'

const initClassifiersStates = async (task: TaskI) => {
    for (let classifier of task.classifiers) {
        classifier.state = defaultClassifierState
    }
    return task
}

export const loadTask = async () => {
    let task: TaskI = {} as TaskI
    await fs.readFile(config.task_file, 'utf8')
        .then(content => {
            task = load(content) as TaskI
        })
        .catch(err => {
            console.log('ERROR loading task:', err)
        })
    return await initClassifiersStates(task)
}

export const loadData = async () => {
    let data: Object[] = [] as Object[]
    await post(config.ep_data, {limit: 0})
        .then(payload => {
            data = payload.data
        })
        .catch(err => {
            console.log('ERROR loading data:', err)
        })
    return data
}