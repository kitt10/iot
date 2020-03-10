function overviewLoaded() {
    startTime();
    ws = new WebSocket('ws://147.228.124.68:8881/websocket')
    ws.onopen = onSocketOpen
    ws.onmessage = onSocketMessage
    ws.onclose = onSocketClose
    firstLoad(load_json_file())
}

function onSocketOpen(event) {
    console.log("WS client: Websocket opened.")
}

function onSocketMessage(message) {
    var data
    try {
        data = JSON.parse(message.data);
        //console.log(data)
        setValuesToFrames(data);
    } catch(e) {
        data = message.data
    }
}

function setValuesToFrames(data) {
    if (data['type'] == 'newSample') {
        if (data['owner'] == 'pn') {
            switch (data['sensor_id']) {
                case 'ds18b20_01':
                    document.getElementsByTagName("temp_in_value")[0].innerHTML = data['value'];
                    set_state_logo("temp_in_state_frame",data['status']);
                    break;
                case 'ds18b20_02':
                    document.getElementsByTagName("temp_out_value")[0].innerHTML = data['value'];
                    set_state_logo("temp_out_state_frame",data['status']);
                    break;   
                case 'dht11_01':
                    document.getElementsByTagName("humidity_value")[0].innerHTML = data['value'];
                    set_state_logo("humidity_state_frame",data['status']);
                    break;   
                case 'tsl2591_01':
                    document.getElementsByTagName("illuminance_value")[0].innerHTML = data['value'].toFixed(0);
                    set_state_logo("luminosity_state_frame",data['status']);
                    break;  
                case 'bme280_01':
                    if (data['quantity'] == 'pressure') {
                        document.getElementsByTagName("pressure_value")[0].innerHTML = data['value']; 
                        set_state_logo("pressure_state_frame",data['status']); }
                    break;   
                case 'am312_01':
                    document.getElementsByTagName("motion_value")[0].innerHTML = data['timestamp'];
                    break;     
                case 'ls311b38_02':
                    document.getElementsByTagName("door_value")[0].innerHTML = formatValue(data['value']);
                    break;
                case 'ls311b38_01':
                    document.getElementsByTagName("window_value")[0].innerHTML = formatValue(data['value']);
                    break;              
            }
        }
    }
}

function firstLoad(data) {
    try {
        document.getElementsByTagName("temp_in_value")[0].innerHTML = data.ds18b20_01[0];
        set_state_logo("temp_in_state_frame",data.ds18b20_01[2]);    
    } catch (e) {
        console.log("Cannot load ds18b20_01 (inside temperature) data.") }
    try {
        document.getElementsByTagName("temp_out_value")[0].innerHTML = data.ds18b20_02[0];
        set_state_logo("temp_out_state_frame",data.ds18b20_02[2]);   
    } catch (e) {
        console.log("Cannot load ds18b20_02 (outside temperature) data.") }
    try {
        document.getElementsByTagName("humidity_value")[0].innerHTML = data.dht11_01[0];
        set_state_logo("humidity_state_frame",data.dht11_01[2]);  
    } catch (e) {
        console.log("Cannot load dht11_01 (inside humidity) data.") }
    try {
        document.getElementsByTagName("illuminance_value")[0].innerHTML = data.tsl2591_01[0].toFixed(0);
        set_state_logo("luminosity_state_frame",data.tsl2591_01[2]);
    } catch (e) {
        console.log("Cannot load tsl2591_01 (illuminance) data.") }
    try {
        document.getElementsByTagName("pressure_value")[0].innerHTML = data.bme280_01[0];
        set_state_logo("pressure_state_frame",data.bme280_01[2]);
    } catch (e) {
        console.log("Cannot load bme280_01 (pressure) data.") }
    try {
        document.getElementsByTagName("motion_value")[0].innerHTML = data.am312_01[1];
    } catch (e) {
        console.log("Cannot load am312_01 (motion) data.") }
    try {
        document.getElementsByTagName("door_value")[0].innerHTML = formatValue(data.ls311b38_02[0]);
    } catch (e) {
        console.log("Cannot load ls311b38_02 (door status) data.") }
    try {
        document.getElementsByTagName("window_value")[0].innerHTML = formatValue(data.ls311b38_01[0]);
    } catch (e) {
        console.log("Cannot load ls311b38_01 (window status) data.") }   
}

function onSocketClose() {
    console.log("WS client: Websocket closed.")
}