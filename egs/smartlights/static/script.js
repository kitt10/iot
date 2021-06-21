var states = {};        // kitt-tip: move to index.html - global JS variables

function onBodyLoad() {
    console.log('GUI loaded.')
    mqtt_connect()
    new_sc_session()
}

function new_sc_session() {
    if (speechcloud) {
        speechcloud.terminate()
    }
    init_speechcloud()
}

function getState(){
    m = "{\"cmd\": \"get_status\"}"
    sendMessage(m, mqtt_topic_cmd)
    setTimeout(makeButtons, 500)
}

function makeButtons(){
    container = document.getElementById("button_container")
    container.innerHTML = ""
    for(light in states){
        container.innerHTML += `<button id=\"${light}\" class=\"light_switch\" onClick=\"toggleLight(this.id)\">${light}</button>`
        var light_button = document.getElementById(light)
        if(states[light] === 1){
           light_button.classList.add("light_on")
        }
        else{
           light_button.classList.add("light_off")
        }
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
                var light_button = document.getElementById(light)
                if(states[light] === 1 && light_button){
                    light_button.classList.add("light_on")
                    light_button.classList.remove("light_off")
                }
                else if(light_button){
                    light_button.classList.replace("light_on", "light_off")
                }
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

function toggleLight(led) {
    msgD = {
        "cmd": "change_status",
        "LED": led,
        "status": 1-states[led]
    }
    msg = JSON.stringify(msgD)
    sendMessage(msg, mqtt_topic_cmd)
}

function debugMode() {
    var mqttMsg = document.getElementById("mqtt_message_target")
    if(mqttMsg.style.visibility === "hidden"){
        mqttMsg.style.visibility = "visible"
    }
    else{
        mqttMsg.style.visibility = "hidden"
    }
}

/*function parseStatement(statement){

}*/