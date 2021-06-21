
/* TTS (Voices: "Iva210", "Jan210", "Jiri210", "Katerina210", "Radka210", "Stanislav210", "Alena210" */
function do_tts(text, voice) {
    speechcloud.tts_synthesize({
        text: text,
        voice: voice
    })
}

/* TTS button listener */
function tts_say_hello() {
    do_tts("Ahoj, toto je stránka projektu Vojtěcha Breníka.", "Iva210")
}

/* ASR button listener */
function asr_start_stop() {
    if (recognizing) {
        speechcloud.asr_pause()
        recognizing = false
        console.log("ASR stopped.")
    } else {
        speechcloud.asr_recognize()
        recognizing = true
        console.log("ASR started: recognizing...")
    }
}

function init_speechcloud(model_uri) {

    /* Space pressed equals ASR button pressed */
    $(window).keydown(function(evt) {
        if (evt.keyCode == 32) {
            evt.preventDefault()
        }
    })

    $(window).keyup(function(evt) {
        if (evt.keyCode == 32) {
            setTimeout(function () {$("#button_asr").click()}, 100);
            evt.preventDefault()
        }
    })

    let options = {
        uri: model_uri,
        tts: "#audio_out",
        disable_audio_processing: true
    }

    let speechcloud = new SpeechCloud(options);

    window.speechcloud = speechcloud

    speechcloud.on('error_init', function (data) {
        console.error('error.init event handler', data.status, data.text)
    })

    speechcloud.on('error_ws_initialized', function () {
        console.log('[WS] - ERROR: WS already initialized.')
    })

    speechcloud.on('_ws_connected', function () {
        console.log('[WS] - connected.')
    })

    speechcloud.on('_ws_closed', function () {
        console.log('[WS] - closed.')
    })

    speechcloud.on('_ws_session', function (data) {
        console.log('[WS] - session started id=' + data.id)
    })

    speechcloud.on('_sip_closed', function (data) {
        console.log('[SIP] - closed.')
    })

    speechcloud.on('_sip_initializing', function (data) {
        console.log('[SIP] - client id=' + data)
    })

    speechcloud.on('_sip_registered', function () {
        console.log('[SIP] - registered.')
    })

    /* ASR ready */
    speechcloud.on('asr_ready', function () {
        console.log("ASR model ready.")
    })

    speechcloud.on('asr_audio_record', function (msg) {
        console.log("Recording...")
    })

    /* ASR result */
    speechcloud.on('asr_result', function (msg) {
        console.log("Got ASR result:", msg)
    })

    /* Update signal */
    speechcloud.on('asr_signal', function (msg) {
        console.log("Received ASR signal:", msg)
    })

    speechcloud.on('sc_start_session', function (msg) {
        session_id = msg.session_id;
        console.log("ASR model: Session ID: " + msg.session_id);
        console.log("ASR model: Session URI: "+ msg.session_uri);
    });

    speechcloud.on('sc_error', function (msg) {
        console.log("Error in method"+msg.method_name+": " + msg.error);
        console.log(msg);
    })

    speechcloud.on('asr_offline_started', function (msg) {
        console.log("asr_offline started.");
    })

    speechcloud.on('asr_offline_finished', function (msg) {
        console.log("asr_offline finished.");
    })

    speechcloud.on('asr_offline_error', function (msg) {
        console.log("asr_offline_error!");
        console.log(msg);
    })

    speechcloud.init()

    console.log('SpeechCloud library initialized.');
}