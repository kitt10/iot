var mqtt
var reconnectTimeout = 2000
var broker = "147.228.124.230"
var port = 9001
var clientID = "WebPageClient"

function onFailure(message) {
    console.log("Connection to Host " + broker + " failed")
    setTimeout(MQTTconnect, reconnectTimeout)
}
	         
function onMessageArrived(msg) {
    json = JSON.parse(msg.payloadString)
    console.log("New message,", msg.destinationName)
} 

function onConnect() {    
    mqtt.subscribe("ite/#")
    console.log("Connected to broker")
}


function sendMessage(m, topic) {  
    message = new Paho.MQTT.Message(m)
	message.destinationName = topic
    mqtt.send(message)
    console.log("Message " + m + " published to topic", topic)
}

function MQTTconnect() {
	console.log("Connecting to " + broker + " " + port)
	mqtt = new Paho.MQTT.Client(broker, port, clientID)
	var options = {
		timeout: 3,
		onSuccess: onConnect,
        onFailure: onFailure
    }
	mqtt.onMessageArrived = onMessageArrived
	mqtt.connect(options)
}