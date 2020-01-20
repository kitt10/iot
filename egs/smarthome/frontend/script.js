function onBodyLoad() {
    ws = new WebSocket('ws://147.228.124.48:8881/websocket')
    ws.onopen = onSocketOpen
    ws.onmessage = onSocketMessage
    ws.onclose = onSocketClose

    reloadModels()
    fillOverview()
}

function onSocketOpen(event) {
    console.log("WS client: Websocket opened.")
}

function onSocketMessage(message) {
    var data
    try {
        data = JSON.parse(message.data)

        if (data['type'] == 'newSample') {
            var quantity = data['quantity']
            var sensor_id = data['sensor_id']
            var value = data['value']
            var timestamp = data['timestamp']
            var classification = data['classification']
            console.log(quantity, sensor_id, value, '::classification:', classification)
            
            try {
                document.getElementById("value_"+quantity+"_"+sensor_id).innerHTML = value+""
                document.getElementById("at_"+quantity+"_"+sensor_id).innerHTML = timestamp
            } catch(e) {
                console.log('E:', e)
            }
        } else if (data['type'] == 'newModelReady') {
            reloadModels()
            showQuantityDetail(selectedRowID)
        }
    } catch(e) {
        data = message.data
    }
    //console.log(data)
}

function onSocketClose() {
    console.log("WS client: Websocket closed.")
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
    request.open("GET", "backend/models.json", false)
    request.send(null)
    models = JSON.parse(request.responseText)
}

function fillOverview() {
    var table = document.getElementById("overview_table")
    var tbody_old = table.tBodies[1]
    var tbody = document.createElement("tbody")
    
    var owners = Object.keys(models).sort()
    for (var owner of owners) {
        var locations = Object.keys(models[owner]).sort()
        for (var location of locations) {
            var quantities = Object.keys(models[owner][location]).sort()
            for (var quantity of quantities) {
                var sensors = models[owner][location][quantity].sensors.sort()
                for (var sensor_id of sensors) {
                    var tr = document.createElement("tr")
                    tr.setAttribute("id", "tr:"+owner+":"+location+":"+quantity+":"+sensor_id)
                    tr.setAttribute("class", "overview_tr")
                    tr.setAttribute("selected", "false")
                    tr.setAttribute("onClick", "showQuantityDetail(this.id)")

                    var td_owner = document.createElement("td")
                    td_owner.appendChild(document.createTextNode(owner))
                    td_owner.setAttribute("class", "owner")
                    tr.appendChild(td_owner)
                    var td_location = document.createElement("td")
                    td_location.appendChild(document.createTextNode(location))
                    td_location.setAttribute("class", "location")
                    tr.appendChild(td_location)
                    var td_quantity = document.createElement("td")
                    td_quantity.appendChild(document.createTextNode(quantity))
                    td_quantity.setAttribute("id", "quantity_"+owner+"_"+location+"_"+quantity+"_"+sensor_id)
                    td_quantity.setAttribute("class", "quantity")
                    tr.appendChild(td_quantity)
                    var td_sensor = document.createElement("td")
                    td_sensor.appendChild(document.createTextNode(sensor_id))
                    td_sensor.setAttribute("id", "sensor_"+quantity+"_"+sensor_id)
                    td_sensor.setAttribute("class", "sensor")
                    tr.appendChild(td_sensor)
                    var td_value = document.createElement("td")
                    td_value.appendChild(document.createTextNode("X"))
                    td_value.setAttribute("id", "value_"+quantity+'_'+sensor_id)
                    td_value.setAttribute("class", "value")
                    tr.appendChild(td_value)
                    var td_at = document.createElement("td")
                    td_at.appendChild(document.createTextNode("X"))
                    td_at.setAttribute("id", "at_"+quantity+'_'+sensor_id)
                    td_at.setAttribute("class", "at")
                    tr.appendChild(td_at)
                    tbody.appendChild(tr)
                }
            }
        }
    }
    table.replaceChild(tbody, tbody_old)
}

function showQuantityDetail(id) {
    selectedRowID = id
    for (var row of document.getElementsByClassName("overview_tr")) {
        row.setAttribute("selected", "false")
    }
    document.getElementById(id).setAttribute("selected", "true")
    console.log('Selected:', id)

    // Available models
    var res = id.split(':')
    var owner = res[1]
    var location = res[2]
    var quantity = res[3]
    var sensor = res[4]
    var available_sensors = models[owner][location][quantity]['sensors'].sort()
    var available_models = Object.keys(models[owner][location][quantity]['available']).sort()
    var active_model = models[owner][location][quantity]['active']

    var table = document.getElementById("available_models_table")
    var tbody_old = table.tBodies[1]
    var tbody = document.createElement("tbody")

    for (model_name of available_models) {
        var metadata = models[owner][location][quantity]['available'][model_name]
        var tr = document.createElement("tr")
        tr.setAttribute("id", "am_"+model_name)
        tr.setAttribute("class", "am_tr")
        tr.setAttribute("selected", model_name == active_model ? "true" : "false")
        tr.setAttribute("onClick", "selectModel(this.id)")

        tr.appendChild(document.createElement("td"))
        var td_from = document.createElement("td")
        td_from.appendChild(document.createTextNode(metadata['date_from']))
        tr.appendChild(td_from)

        var td_to = document.createElement("td")
        td_to.appendChild(document.createTextNode(metadata['date_to']))
        tr.appendChild(td_to)

        var td_sensors = document.createElement("td")
        td_sensors.appendChild(document.createTextNode(metadata['sensors']))
        tr.appendChild(td_sensors)

        var td_nsamples = document.createElement("td")
        td_nsamples.appendChild(document.createTextNode(metadata['n_samples']))
        tr.appendChild(td_nsamples)

        tbody.appendChild(tr)
    }
    table.replaceChild(tbody, tbody_old)

    var td_sensors_available = document.getElementById("td_sensors_available")
    while (td_sensors_available.firstChild) {
        td_sensors_available.removeChild(td_sensors_available.firstChild);
    }

    for (available_sensor of available_sensors) {
        var cb = document.createElement("input")
        cb.type = "checkbox"
        cb.id = "cb:"+available_sensor
        cb.value = available_sensor
        cb.checked = true
        td_sensors_available.appendChild(cb)

        var label = document.createElement("label")
        label.setAttribute("for", cb.id)
        label.innerHTML = available_sensor
        td_sensors_available.appendChild(label)
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
        title: owner+" / "+location+" / "+quantity+" / "+sensor,
        xaxis: {
            //tickmode: "linear",
            //tick0: 0,
            //dtick: 3600
            tickmode: 'array',
            tickvals: [0, 3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000, 75600, 79200, 82800, 86400],
            ticktext: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        }
    }
    Plotly.newPlot('detail_plot', plot_data, layout)
}

function onRetrain() {
    var res = selectedRowID.split(':')
    var owner = res[1]
    var location = res[2]
    var quantity = res[3]

    var sensors_selected = []
    for (el of document.getElementById("td_sensors_available").childNodes) {
        if (el.nodeName == "INPUT" && el.checked) {
            sensors_selected.push(el.value)
        }
    }

    var params = {
        type: "newModel",
        owner: owner,
        topic: "smarthome/"+location+"/"+quantity,
        sensors: sensors_selected,
        date_from: document.getElementById("input_date_from").value,
        date_to: document.getElementById("input_date_to").value
    }
    ws.send(JSON.stringify(params))
}

function selectModel(id) {
    model_name = id.substring(3)
    var params = {
        type: "selectModel",
        model_name: model_name
    }
    ws.send(JSON.stringify(params))
}