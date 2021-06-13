
function init_speechcloud(model_uri) {
    var options = {
        uri: model_uri,
        //tts: "#audioout",
        disable_audio_processing: false
    };

    speech_cloud = new SpeechCloud(options)

    speech_cloud.on('error_init', function (data) {
        console.error('error.init event handler', data.status, data.text)
    });

    speech_cloud.on('error_ws_initialized', function () {
        console.log('[WS] - ERROR: WS already initialized.')
    });

    speech_cloud.on('_ws_connected', function () {
        console.log('[WS] - connected.')
    });

    speech_cloud.on('_ws_closed', function () {
        console.log('[WS] - closed.')
    });

    speech_cloud.on('_ws_session', function (data) {
        console.log('[WS] - session started id=' + data.id)
    });

    speech_cloud.on('_sip_closed', function (data) {
        console.log('[SIP] - closed.')
    });

    speech_cloud.on('_sip_initializing', function (data) {
        console.log('[SIP] - client id=' + data)
    });

    speech_cloud.on('_sip_registered', function () {
        console.log('[SIP] - registered.')
    });

    /* ASR ready */
    speech_cloud.on('asr_ready', function () {
        console.log("ASR model ready.")
    });

    speech_cloud.on('asr_audio_record', function (msg) {
        console.log("Recording...")
    });

    /* ASR result */
    speech_cloud.on('asr_result', function (msg) {
        console.log("Got ASR result:", msg)
    });

    /* Update signal */
    speech_cloud.on('asr_signal', function (msg) {
        console.log("Received ASR signal:", msg)
    });

    speech_cloud.on('sc_start_session', function (msg) {
        session_id = msg.session_id;
        console.log("ASR model: Session ID: " + msg.session_id);
        console.log("ASR model: Session URI: "+ msg.session_uri);
    });

    speech_cloud.on('sc_error', function (msg) {
        console.log("Error in method"+msg.method_name+": " + msg.error);
        console.log(msg);
    });

    speech_cloud.on('asr_offline_started', function (msg) {
        console.log("asr_offline started.");
    });

    speech_cloud.on('asr_offline_finished', function (msg) {
        console.log("asr_offline finished.");
    });

    speech_cloud.on('asr_offline_error', function (msg) {
        console.log("asr_offline_error!");
        console.log(msg);
    });

    speech_cloud.init();

    console.log('Speech cloud library initialized.');
}