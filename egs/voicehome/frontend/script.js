
function onBodyLoad() {
    console.log('Web GUI loaded.')
    ws = new WebSocket('ws://localhost:8881/websocket')     // ws is a global variable (index.html)
    ws.onopen = onSocketOpen
    ws.onmessage = onSocketMessage
    ws.onclose = onSocketClose
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
        message: message,
        second_param: [1, 2]
    }
    ws.send(JSON.stringify(payload))
}