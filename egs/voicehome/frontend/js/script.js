
function onBodyLoad() {
    console.log('Web GUI loaded.')
    ws = new WebSocket('ws://147.228.124.230:8881/websocket')     // ws is a global variable (index.html)
    ws.onopen = onSocketOpen
    ws.onmessage = onSocketMessage
    ws.onclose = onSocketClose
    //fillModules()
}

function onSocketOpen() {
    console.log("WS client: Websocket opened.")
}

function onSocketMessage(message) {
    let data
    try {
        data = JSON.parse(message.data)
    } catch(e) {
        data = message.data
    }
    console.log("WS message:", data)
    sendToServer("Hi from browser. Got your message.")
}

function onSocketClose() {
    console.log("WS client: Websocket closed.")
}

function sendToServer(message) {
    let payload = {
        passport: "system/test",
        message: message
    }
    ws.send(JSON.stringify(payload))
}

function loadJsonHandler() {
    let xmlhttp
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    }
    xmlhttp.open('GET', '/packet', false);
    xmlhttp.send(null);

    return  JSON.parse(xmlhttp.responseText);
}

function fillModules() {
    let modules = loadJsonHandler().modules
    let divModules = document.getElementById('modules')

    for (let i_module=0; i_module<modules.length; i_module++) {
        let moduleDiv = document.createElement("DIV")
        moduleDiv.className = 'module'

        let moduleTitleDiv = document.createElement("DIV")
        moduleTitleDiv.className = 'module_title'
        moduleTitleDiv.innerHTML = modules[i_module].module_id
        moduleDiv.appendChild(moduleTitleDiv)

        let moduleDescriptionDiv = document.createElement("DIV")
        moduleDescriptionDiv.className = 'module_description'
        moduleDescriptionDiv.innerHTML = modules[i_module].description
        moduleDiv.appendChild(moduleDescriptionDiv)

        let moduleMovesDiv = document.createElement("DIV")
        moduleMovesDiv.className = 'module_moves'
        moduleDiv.appendChild(moduleMovesDiv)

        divModules.appendChild(moduleDiv)

        for (let i_move=0; i_move<modules[i_module].moves.length; i_move++) {
            let moveDiv = document.createElement("DIV")
            moveDiv.className = 'move'

            let moveTitleDiv = document.createElement("DIV")
            moveTitleDiv.className = 'move_title'
            moveTitleDiv.innerHTML = modules[i_module].moves[i_move].method_name
            moveDiv.appendChild(moveTitleDiv)

            let moveDescriptionDiv = document.createElement("DIV")
            moveDescriptionDiv.className = 'move_description'
            moveDescriptionDiv.innerHTML = modules[i_module].moves[i_move].description
            moveDiv.appendChild(moveDescriptionDiv)

            let moveCallsDiv = document.createElement("DIV")
            moveCallsDiv.className = 'move_calls'
            moveDiv.appendChild(moveCallsDiv)

            moduleMovesDiv.appendChild(moveDiv)

            for (let i_call=0; i_call<modules[i_module].moves[i_move].calls.length; i_call++) {
                let moveCallDiv = document.createElement("DIV")
                moveCallDiv.className = 'move_call'
                moveCallDiv.innerHTML = modules[i_module].moves[i_move].calls[i_call].toString().replace(',', ' ')
                moveCallsDiv.appendChild(moveCallDiv)
            }
        }
    }
}