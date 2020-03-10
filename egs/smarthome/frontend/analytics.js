function analyticsLoaded() {
    ws = new WebSocket('ws://147.228.124.68:8881/websocket')
    ws.onopen = onSocketOpen
    ws.onmessage = onSocketMessage
    ws.onclose = onSocketClose
    updateTitle("to show model details please select owner")
    reloadModels()
}

function onSocketOpen(event) {
    console.log("WS client: Websocket opened.")
}

function onSocketMessage(message) {
    var data
    try {
        data = JSON.parse(message.data)
        updateValuesSensorDetail(data);
    } catch(e) {
        data = message.data
    }
    //console.log(data)
}

function onSocketClose() {
    console.log("WS client: Websocket closed.")
}

function updateValuesSensorDetail(data) {
    if (showingSensorValues) {
        if (data['type'] == 'newSample') {
            if (data['owner'] == 'pn') {
                if (data['sensor_id'] == selectedSensorId) {
                    document.getElementsByTagName("last_value_frame")[0].innerHTML = data['value'];
                    document.getElementsByTagName("at_timestamp_frame")[0].innerHTML = data['timestamp'];
                    set_state_logo("sensor_status_frame",data['status']);
                }
            }
        }
    }
}    

function fillLocationOptions() {
    var f=0
    if (selectedOwner == "pn") {
        locationOptions = ["room", "outside"];
        for (f = 0; f < locationOptions.length; f++) {
            var node = document.createElement("option");
            node.setAttribute("value",f)
            var textnode = document.createTextNode(locationOptions[f]);
            node.appendChild(textnode);
            document.getElementById("location").appendChild(node);
            //console.log(node)
        }   
    }
}

function fillQuantityOptions() {
    var f=0
    if (selectedLocation == "room") {
        quantityOptions = ["temperature","illuminance","humidity","pressure","motion","door_open","window_open"];
    } else if (selectedLocation == "outside") {  
        quantityOptions = ["temperature"];    
    }
    for (f = 0; f < quantityOptions.length; f++) {
        var node = document.createElement("option");
        node.setAttribute("value",f)
        var textnode = document.createTextNode(quantityOptions[f]);
        node.appendChild(textnode);
        document.getElementById("quantity").appendChild(node);
        //console.log(node)
    }   
}

function fillSensorIdOptions() {
    var f=0
    if (selectedLocation == "room") {
        switch (selectedQuantity) {
            case "temperature":
                sensorIdOptions = ["ds18b20_01","bme280_01"];
                break;
            case "illuminance":
                sensorIdOptions = ["tsl2591_01"];
                break;
            case "humidity":
                sensorIdOptions = ["dht11_01"];
                break;
            case "pressure":
                sensorIdOptions = ["bme280_01"];
                break;
            case "motion":
                sensorIdOptions = ["am312_01"];
                break;  
            case "door_open":
                sensorIdOptions = ["ls311b38_02"];         
                break;
            case "window_open":
                sensorIdOptions = ["ls311b38_01"];  
                break;    
        }
    } else if (selectedLocation == "outside") {  
        switch (selectedQuantity) {
            case "temperature":
                sensorIdOptions = ["ds18b20_02"];
            break;
        } 
    }    
    for (f = 0; f < sensorIdOptions.length; f++) {
        var node = document.createElement("option");
        node.setAttribute("value",f)
        var textnode = document.createTextNode(sensorIdOptions[f]);
        node.appendChild(textnode);
        document.getElementById("sensorId").appendChild(node);
        //console.log(node)
    }
}

function GetSelectedOwner(){
    var e = document.getElementById("owner");
    var result = e.options[e.selectedIndex].text;
    if (result != "owner") {
        selectedOwner = result
        fillLocationOptions()
        updateTitle("to show model details please select location")
        //console.log(result)
    }    
}

function GetSelectedLocation(){
    var e = document.getElementById("location");
    var result = e.options[e.selectedIndex].text;
    if (result != "location") {
        selectedLocation = result
        fillQuantityOptions()
        updateTitle("to show model details please select quantity")
        //console.log(result)
    } 
}

function GetSelectedQuantity() {
    var e = document.getElementById("quantity");
    var result = e.options[e.selectedIndex].text;
    if (result != "quantity") {
        selectedQuantity = result
        fillSensorIdOptions()
        updateTitle("to show model details please select sensor id")
        //console.log(result)
    } 
}

function GetSelectedSensorId() {
    var e = document.getElementById("sensorId");
    var result = e.options[e.selectedIndex].text;
    if (result != "sensor id") {
        selectedSensorId = result
        //console.log(result)
        showQuantityDetail("tr:"+selectedOwner+":"+selectedLocation+":"+selectedQuantity+":"+selectedSensorId)
        showNSamples("tr:"+selectedOwner+":"+selectedLocation+":"+selectedQuantity+":"+selectedSensorId)
        updateGraphTitle(selectedOwner,selectedLocation,selectedQuantity,selectedSensorId) 
        updateSensorInfo(selectedSensorId.split("_")[0]) //remove sensor number from sensor id - for example "ds18b20_01" -> "ds18b20"
        loadSensorValues(selectedSensorId)
    }
}

function loadSensorValues(selectedSensorId) {
    loadLastValue(load_json_file(),selectedSensorId)  
    loadAtTimestamp(load_json_file(),selectedSensorId)
    loadSensorStatus(load_json_file(),selectedSensorId)
    showingSensorValues = true
}    

function resetDropdownMenu() {
    updateTitle("to show model details please select owner")
    
    var elements = document.getElementsByTagName('select');
    for (var i = 0; i < elements.length; i++) {
      elements[i].selectedIndex = 0;
    }
    removeChild("location")
    removeChild("quantity")
    removeChild("sensorId")
}

function removeChild(elementId) {
    var select = document.getElementById(elementId);
    try {
      while (select.hasChildNodes()) {
        select.removeChild(select[1]);
      }
    } catch (TypeError) {
        console.log("childs removed.")
    }
}

function updateGraphTitle(owner,location,quantity,sensor) {
    document.getElementsByTagName("graph_title")[0].innerHTML = owner + " / " + location + " / " + quantity + " / " + sensor;
}   

function updateTitle(text) {
    document.getElementsByTagName("graph_title")[0].innerHTML = text;
}

function updateSensorInfo(selectedSensorId) {
    switch (selectedSensorId) {
        case "ds18b20":
            document.getElementsByTagName("quantity_detail_frame1")[0].style.backgroundColor = "rgba(0, 0, 0, 0.5)";
            document.getElementsByTagName("quantity_detail_frame1")[0].innerHTML = "sensor ds18b20" + "<br />" 
                                                                                +  "voltage range: 3.0 V - 5.5 V" + "<br />"
                                                                                +  "temperature range: -55 °C to +125 °C" + "<br />"
                                                                                +  "accuracy: ± 0.5 from -10 °C to +85 °C";
            setQuantityDetailFrame2()
            break;
        case "dht11":
            document.getElementsByTagName("quantity_detail_frame1")[0].style.backgroundColor = "rgba(0, 0, 0, 0.5)";
            document.getElementsByTagName("quantity_detail_frame1")[0].innerHTML = "sensor dht11" + "<br />" 
                                                                                +  "voltage range: 3.0 V - 5.5 V" + "<br />"
                                                                                +  "humidity range: 20 % to 90 %" + "<br />"
                                                                                +  "accuracy: ± 5.0 %";
            setQuantityDetailFrame2()
            break;
        case "bme280":
            document.getElementsByTagName("quantity_detail_frame1")[0].style.backgroundColor = "rgba(0, 0, 0, 0.5)";
            document.getElementsByTagName("quantity_detail_frame1")[0].innerHTML = "sensor bme280" + "<br />" 
                                                                                +  "voltage range: 1.71 V - 3.6 V" + "<br />"
                                                                                +  "temperature range: -40 °C to +85 °C" + "<br />"
                                                                                +  "barometric pressure range: 300 hPa to 1100 hPa" + "<br />";
            setQuantityDetailFrame2()
            break;   
        case "tsl2591":
            document.getElementsByTagName("quantity_detail_frame1")[0].style.backgroundColor = "rgba(0, 0, 0, 0.5)";
            document.getElementsByTagName("quantity_detail_frame1")[0].innerHTML = "sensor tsl2591" + "<br />" 
                                                                                +  "voltage range: 2.7 V - 3.6 V" + "<br />"
                                                                                +  "temperature range: -30 °C to +80 °C" + "<br />"
                                                                                +  "luminosity range: 188 μLux to 88.000 Lux" + "<br />";
            setQuantityDetailFrame2()
            break;    
        case "ls311b38":
            document.getElementsByTagName("quantity_detail_frame1")[0].style.backgroundColor = "rgba(0, 0, 0, 0.5)";
            document.getElementsByTagName("quantity_detail_frame1")[0].innerHTML = "sensor ls311b38" + "<br />" 
                                                                                +  "max voltage: 100 V" + "<br />"
                                                                                +  "max current: 500 mA" + "<br />"
                                                                                +  "operating distance: 15 - 20 mm" + "<br />";
            setQuantityDetailFrame2()
            break; 
        case "am312":
            document.getElementsByTagName("quantity_detail_frame1")[0].style.backgroundColor = "rgba(0, 0, 0, 0.5)";
            document.getElementsByTagName("quantity_detail_frame1")[0].innerHTML = "sensor am312" + "<br />" 
                                                                                +  "voltage range: 2.7 - 12 V" + "<br />"
                                                                                +  "operating distance: 3 - 5 m" + "<br />"
                                                                                +  "degree of detection: < 100°" + "<br />";
            setQuantityDetailFrame2()                                                                    
            break;                    
    }        
}

function setQuantityDetailFrame2() {
    document.getElementsByTagName("quantity_detail_frame2")[0].style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    document.getElementsByTagName("quantity_detail_frame2")[0].innerHTML = "number of samples:"  + "<br />" 
                                                                        +  "last value: " + "<br />"
                                                                        +  "at timestamp: " +  "<br />"
                                                                        +  "sensor status: " +  "<br />";   
}


function loadJsonClf(owner, location, quantity, sensor_id) {
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest()
    }
    xmlhttp.open('GET', '/json_clfs/', false)
    xmlhttp.send(null);

    return  JSON.parse(xmlhttp.responseText)[owner][location][quantity][sensor_id]
}

function reloadModels() {
    var request = new XMLHttpRequest();
    request.open("GET", "../backend/models.json", false)
    request.send(null)
    models = JSON.parse(request.responseText)
}

function showNSamples(id) {
    var res = id.split(':')
    var owner = res[1]
    var location = res[2]
    var quantity = res[3]
    var available_models = Object.keys(models[owner][location][quantity]['available']).sort()
    for (model_name of available_models) {
        var metadata = models[owner][location][quantity]['available'][model_name]
        document.getElementsByTagName("n_samples_frame")[0].innerHTML = metadata['n_samples'];
    }
}   

function loadLastValue(data,selectedSensorId) {
    try {
        document.getElementsByTagName("last_value_frame")[0].innerHTML = data[selectedSensorId][0];
    } catch (e) {
        console.log("Cannot load " + selectedSensorId + " data.") 
   }
}

function loadAtTimestamp(data,selectedSensorId) {
    try {
        document.getElementsByTagName("at_timestamp_frame")[0].innerHTML = data[selectedSensorId][1];
    } catch (e) {
        console.log("Cannot load " + selectedSensorId + " data.") 
    }
}   

function loadSensorStatus(data,selectedSensorId) {
    try {
        set_state_logo("sensor_status_frame",data[selectedSensorId][2]);     
    } catch (e) {
        console.log("Cannot load " + selectedSensorId + " data.") 
    }
} 

function showQuantityDetail(id) {
    selectedRowID = id
    for (var row of document.getElementsByClassName("overview_tr")) {
        row.setAttribute("selected", "false")
    }
    console.log('Selected:', id)

    // Available models
    var res = id.split(':')
    var owner = res[1]
    var location = res[2]
    var quantity = res[3]
    var sensor = res[4]
    var available_sensors = models[owner][location][quantity]['sensors'].sort()
    var td_sensors_available = [] 

    for (available_sensor of available_sensors) {
        td_sensors_available.push(available_sensor);
    }

    // Load CLF data and sensory data
    data = loadJsonClf(owner, location, quantity, sensor)
    if (data['dim'] == 1) {
        var plot_data = [{
            y: data['model'], 
            x: data['x'],
            type: 'scatter'
            },
            {
            x: data['samples_x'],
            y: data['samples_y'],
            type: 'scatter',
            mode: 'markers',
            marker: {
                size: 2,
                color: data['samples_color']
            }
            }
        ]
    } else if (data['dim'] == 2) {
        var plot_data = [{
            z: data['model'], 
            x: data['x'], 
            y: data['y'],
            type: 'contour'
            },
            {
            x: data['samples_x'],
            y: data['samples_y'],
            type: 'scatter',
            mode: 'markers',
            marker: {
                size: 2,
                color: data['samples_color']
            }
            }
        ]
    }

    var layout = {
        xaxis: {
            tickmode: 'array',
            tickvals: [0, 3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000, 75600, 79200, 82800, 86400],
            ticktext: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        }
    }
    Plotly.newPlot('selected_data_detail', plot_data, layout)
    updateGraphTitle(owner,location,quantity,sensor)
}