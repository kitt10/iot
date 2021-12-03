import { getCurrentTs } from "./fcn/_tools"

const config = {
    task_file: '../engine/task.yaml',
    ep_data: 'http://localhost:9777/ep_data/',
    ep_control: 'http://localhost:9777/ep_control/',
    ep_train: 'http://localhost:9777/ep_train/',

    defaultTrainBack: 1638313200.0,                  // 1.12.2021
    defaultShowBack: getCurrentTs() - 1800           // last 30 minutes
}

export default config