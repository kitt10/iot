function onBodyLoad() {
    console.log('GUI loaded.')
    mqtt_connect()
    new_sc_session()
}

function new_sc_session() {
    if (speech_cloud) {
        speech_cloud.terminate()
    }
    init_speechcloud(sc_model_uri)
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
    console.log(`Toggled ${led}.`)
    sendMessage(msg, mqtt_topic_cmd)
}

function lightOn(led) {
    msgD = {
        "cmd": "change_status",
        "LED": led,
        "status": 1
    }
    msg = JSON.stringify(msgD)
    console.log(`Turned ${led} on.`)
    sendMessage(msg, mqtt_topic_cmd)
}

function lightOff(led) {
    msgD = {
        "cmd": "change_status",
        "LED": led,
        "status": 0
    }
    msg = JSON.stringify(msgD)
    console.log(`Turned ${led} off.`)
    sendMessage(msg, mqtt_topic_cmd)
}

function debugMode() {
    var dbg = document.getElementsByClassName("dbg")
    visibility = "";
    console.log(dbg)

    if(dbg[0].style.visibility === "visible"){
        visibility = "hidden"
    }
    else{
        visibility = "visible"
    }
    for(i=0;i<dbg.length;i++){
        console.log(dbg[i])
        dbg[i].style.visibility = visibility;
    }
}

function parseStatement(statement){
    console.log(statement)
    rLight = "(bíl|zelen|červen|svět|led|diod)(á|é(ho)?|ou|la|el|ky|ek|y)?( (ledk(a|u|y)|svět(lo|la)|diod(a|u|y)))?"
    rOn = new RegExp("(((rozsviť)|(rozsvítit)|zapni|zapnout) ("+rLight+"))|((ať( se)?) ("+rLight+") ((roz)?svítí))|zapn(e|ou)")
    rOff = new RegExp("(((zhasni)|(zhasnout)|vypni|vypnout) ("+rLight+"))|((ať( se)?) ("+rLight+") ((zhasne)|(nesvítí)|vypn(e|ou)))")
    rState = new RegExp("(((jaký je )?(aktuální|současný|nyní|teď)? ?stav)|(je)|(svítí)|jsou) ("+rLight+")(( rozsvícen(á|é))| zhasnut(á|é)| (zap|vyp)nut(á|é))?")
    rToggle = new RegExp("(přepn(i|out)) ("+rLight+")")

    if(match = statement.match(rOn)){
        if(!(color = match[6])) color = match[18]; //color is in group 6 or 18
        console.log(`matched on, color: ${color}`)
        if(["svět", "diod", "led"].includes(color)){
            for(led in states){
                lightOn(led)
            }
        }
        else{
            if(color == "bíl") lightOn("WHITE");
            else if(color == "červen") lightOn("RED");
            else if(color == "zelen") lightOn("GREEN");
        }
    }
    else if(match = statement.match(rOff)){
        if(!(color = match[6])) color = match[18]; //color is in group 6 or 18
        console.log(`matched off, color: ${color}`)
        if(["svět", "diod", "led"].includes(color)){
            for(led in states){
                lightOff(led)
            }
        }
        else{
            if(color == "bíl") lightOff("WHITE");
            else if(color == "červen") lightOff("RED");
            else if(color == "zelen") lightOff("GREEN");
        }
    }
    else if(match = statement.match(rState)){
        color = match[8]
        if(["svět", "diod", "led"].includes(color)){
            reportState(["WHITE", "RED", "GREEN"])
        }
        else{
            if(color == "bíl") reportState("WHITE");
            else if(color == "červen") reportState("RED");
            else if(color == "zelen") reportState("GREEN");
        }
    }
    else if(match = statement.match(rToggle)){
        color = match[3]
        if(["svět", "diod", "led"].includes(color)){
            for(led in states){
                toggleLight(led)
            }
        }
        else{
            if(color == "bíl") toggleLight("WHITE");
            else if(color == "červen") toggleLight("RED");
            else if(color == "zelen") toggleLight("GREEN");
        }
    }
    else{
        console.log("Didn't match anything")
    }
}

function reportState(leds){
    console.log(`reporting state of ${leds}`)
    report = ""
    ledsCZ = {"WHITE": "bílá", "RED": "červená", "GREEN": "zelená"}
    for(led in leds){
        if(report.length) report+=", ";
        report += `${ledsCZ[led]} ${states[led]?"svítí":"nesvítí"}` 
    }
    report+="."
    //call TTS func on report
}