var states = {};

function onBodyLoad() {
    console.log('GUI loaded.')
    mqtt_connect()
}

function getState(){
    m = "{\"cmd\": \"get_status\"}"
    sendMessage(m, mqtt_topic_cmd)
    setTimeout(makeButtons, 500)
}

function makeButtons(){
    container = document.getElementById("button-container")
    container.innerHTML = ""
    for(light in states){
        container.innerHTML += `<button id=\"${light}\" class=\"light-switch\" onClick=\"toggleLight(this)\">${light}</button>`
    }
}

function sendAhoy() {
    sendMessage("GUI is connected to MQTT - hello.", "smartlights/hello")
}

function onFailure(message) {
    console.log("Connection to Host " + mqtt_broker + " failed")
    setTimeout(mqtt_connect, mqtt_reconnect_timeout)
}

function onMessageArrived(msg) {
    console.log("New MQTT message:", msg)
    console.log(msg.payloadString)
    try{
        msgD = JSON.parse(msg.payloadString)
        if("states" in msgD){
            for(light in msgD.states){
                states[light] = msgD.states[light]
            }
        }
    }
    catch(err){

    }
    
    document.getElementById("mqtt_message_target").innerHTML = msg.payloadString
}

function onConnect() {
    mqtt_client.subscribe(mqtt_topic_subscribe)
    console.log("Connected to MQTT broker. Subscribed:", mqtt_topic_subscribe)
    sendAhoy()
    getState()
}

function sendMessage(m, topic) {
    message = new Paho.MQTT.Message(m)
	message.destinationName = topic
    mqtt_client.send(message)
    console.log("MQTT message " + m + " published to topic", topic)
}

function mqtt_connect() {
	console.log("Connecting to " + mqtt_broker + ":" + mqtt_port)
	mqtt_client = new Paho.MQTT.Client(mqtt_broker, mqtt_port, mqtt_client_id)
	var options = {
        userName: mqtt_username,
        password: mqtt_passwd,
		timeout: 3,
		onSuccess: onConnect,
        onFailure: onFailure
    }
	mqtt_client.onMessageArrived = onMessageArrived
	mqtt_client.connect(options)
}

function toggleLight(element) {
    msgD = {
        "cmd": "change_status",
        "LED": element.id,
        "status": 1-states[element.id]
    }
    msg = JSON.stringify(msgD)
    sendMessage(msg, mqtt_topic_cmd)
}