function onBodyLoad() {
    ws = new WebSocket('ws://localhost:8881/websocket')
    ws.onopen = onSocketOpen
    ws.onmessage = onSocketMessage
    ws.onclose = onSocketClose
}

function onSocketOpen(event) {
    console.log("WS client: Websocket opened.")
}

function onSocketMessage(message) {
    var data
    try {
        data = JSON.parse(message.data)
    } catch(e) {
        data = message.data
    }
    console.log(data)
}

function onSocketClose() {
    console.log("WS client: Websocket closed.")
}