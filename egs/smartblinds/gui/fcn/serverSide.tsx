import { load } from 'js-yaml'
import fs from 'promise-fs'
import { TaskI } from '../context/TaskContext'

export const loadTask = async () => {
    let task: TaskI = {} as TaskI
    await fs.readFile('../engine/task.yaml', 'utf8')
        .then(content => {
            task = load(content) as TaskI
        })
        .catch(err => {
            console.log('ERROR loading task:', err)
        })
    return task
}