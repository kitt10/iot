import { getCurrentTs } from "./fcn/_tools"

//const engineURL = 'http://localhost'              // your local
const engineURL = 'http://147.228.124.48'           // kitt-kky
const enginePort = '9777'                           // take it from ../engine/cfg_engine.yml

const config = {
    task_file: '../engine/task.yaml',
    ep_data: engineURL+':'+enginePort+'/ep_data/',
    ep_control: engineURL+':'+enginePort+'/ep_control/',
    ep_train: engineURL+':'+enginePort+'/ep_train/',

    defaultTrainBack: 1638313200.0,                  // 1.12.2021
    defaultShowBack: getCurrentTs() - 18000,         // last 5 hours
}

export default config