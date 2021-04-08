function onBodyLoad() {
    console.log('GUI loaded.')
    mqtt_connect()
}

function onFailure(message) {
    console.log("Connection to Host " + mqtt_broker + " failed")
    setTimeout(mqtt_connect, mqtt_reconnect_timeout)
}

function onMessageArrived(msg) {
    json = JSON.parse(msg.payloadString)
    console.log("New MQTT message:", msg.destinationName)

    document.getElementById("mqtt_message_target").innerHTML = json
}

function onConnect() {
    mqtt_client.subscribe(mqtt_topic_subscribe)
    console.log("Connected to MQTT broker. Subscribed:", mqtt_topic_subscribe)
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