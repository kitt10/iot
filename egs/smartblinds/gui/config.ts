import { getCurrentTs } from "./fcn/_tools"

const engineProtocol = 'http'
const WSProtocol = 'ws'

//const engineHost = 'localhost'              // your local
const engineHost = '147.228.124.48'           // kitt-kky

const enginePort = '9777'                           // take it from ../engine/cfg_engine.yml
const engineURL = `${engineProtocol}://${engineHost}:${enginePort}`

const config = {
    task_file: '../engine/task.yaml',
    ep_data: engineURL+'/ep_data/',
    ep_control: engineURL+'/ep_control/',
    ep_train: engineURL+'/ep_train/',
    ep_ws: `${WSProtocol}://${engineHost}:${enginePort}/ws/`,

    defaultTrainBack: 1638313200.0,                  // 1.12.2021
    defaultShowBack: getCurrentTs() - 1209600,       // last 14 days
}

export default config
