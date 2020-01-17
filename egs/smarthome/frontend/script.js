function onBodyLoad() {
    ws = new WebSocket('ws://localhost:8881/websocket')
    ws.onopen = onSocketOpen
    ws.onmessage = onSocketMessage
    ws.onclose = onSocketClose

    reloadModels()
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
        } else if (data['type'] == 'aDetail') {
            console.log('AM HERE.')
            console.log(data)
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

            var layout = {
                title: data['owner']+" / "+data['location']+" / "+data['quantity'],
                xaxis: {
                    tickmode: "linear",
                    tick0: 0,
                    dtick: 3600
                }
            }
            Plotly.newPlot('detail_plot', plot_data, layout)
        }

        
    } catch(e) {
        data = message.data
    }
    //console.log(data)
}

function onSocketClose() {
    console.log("WS client: Websocket closed.")
}

function reloadModels() {
    var request = new XMLHttpRequest();
    request.open("GET", "backend/models.json", false)
    request.send(null)
    models = JSON.parse(request.responseText)

    fillOverview()
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
        td_sensors_available.appendChild(cb)
    }

    // Load CLF data and sensory data
    var params = {
        type: "getDetail",
        owner: owner,
        location: location,
        quantity: quantity,
        sensor_id: sensor
    }
    ws.send(JSON.stringify(params))
}

function onRetrain() {
    var res = selectedRowID.split(':')
    var owner = res[1]
    var location = res[2]
    var quantity = res[3]

    var params = {
        type: "retrainModel",
        owner: owner,
        topic: "smarthome/"+location+"/"+quantity,
        sensors: ["ls311b38_02"],
        date_start: "2019-12-10",
        date_end: "2019-12-15"
    }
    ws.send(JSON.stringify(params))
}