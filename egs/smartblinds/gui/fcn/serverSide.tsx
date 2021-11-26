import { load } from 'js-yaml'
import fs from 'promise-fs'
import { post } from './httpFetch'
import { TaskI } from '../context/TaskContext'
import config from '../config'

export const loadTask = async () => {
    let task: TaskI = {} as TaskI
    await fs.readFile(config.task_file, 'utf8')
        .then(content => {
            task = load(content) as TaskI
        })
        .catch(err => {
            console.log('ERROR loading task:', err)
        })
    return task
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