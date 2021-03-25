// Global variables
// var dataTemperature = [];
var sensorsListFull = {};
var sensorsState = {};
var dataTemperatureFull = [];
var dataTemperature = "";
var dataPressureFull = [];
var dataPressure = "";
var dataIlluminanceFull = [];
var dataIlluminance = "";
var MAXROOM;
var page = "home";
var controller_state = {};

var ws_address = "ws://147.228.124.230:8881/websocket";
// var ws_address = "ws://127.0.0.1:8881/websocket";

function onBodyLoadModules() {
	page = "modules";
	console.log("Web GUI loaded.");
	ws = new WebSocket(ws_address); // ws is a global variable (index.html)
	ws.onopen = onSocketOpen;
	ws.onmessage = onSocketMessage;
	ws.onclose = onSocketClose;

	fillModules();
	drawControllersState();
}

function onBodyLoad() {
	page = "home";
	console.log("Web GUI loaded.");
	ws = new WebSocket(ws_address); // ws is a global variable (index.html)
	ws.onopen = onSocketOpen;
	ws.onmessage = onSocketMessage;
	ws.onclose = onSocketClose;

	drawControllersState();
}

function turnModuleOnOff(on, module_id) {
	let payload = {
		passport: on ? "module_on" : "module_off",
		module_id: module_id,
	};
	ws.send(JSON.stringify(payload));
}

function get_controller_id() {
	return loadJsonHandler().controller_id;
}

function onBodyLoadAnalytics() {
	page = "analytics";
	console.log("onBodyLoadAnalytics");
	console.log("Web GUI loaded.");
	ws = new WebSocket(ws_address); // ws is a global variable (index.html)
	ws.onopen = onSocketOpen;
	ws.onmessage = onSocketMessage;
	ws.onclose = onSocketClose;

	drawControllersState();
	// request_sensorsList();
	// request_whole_temperature_data();
	// request_sensorsList();
	// request_whole_temperature_data();
	// request_whole_pressure_data();
}

function onSocketOpen() {
	console.log("WS client: Websocket opened.");
}

function drawControllersState() {
	if (!jQuery.isEmptyObject(controller_state)) {
		if (controller_state.passport == "controller_connected") {
			if (controller_state.controller_id == "keyboard") {
				$("#controllers_state")
					.attr("src", "/img/controller_icons/keyboard_on.svg")
					.attr("alt", "keyboard_on");
			} else {
				$("#controllers_state")
					.attr("src", "/img/controller_icons/voicekit_on.svg")
					.attr("alt", "voicekit_on");
			}
		}
		if (controller_state.passport == "controller_disconnected") {
			$("#controllers_state").attr("src", "").attr("alt", "");
		}
	} else {
		switch (get_controller_id()) {
			case "keyboard":
				$("#controllers_state")
					.attr("src", "/img/controller_icons/keyboard_on.svg")
					.attr("alt", "keyboard_on");
				break;
			case "voicekit":
				$("#controllers_state")
					.attr("src", "/img/controller_icons/voicekit_on.svg")
					.attr("alt", "voicekit_on");
				break;
			default:
				break;
		}
	}
}

function onSocketMessage(message) {
	let data;
	try {
		data = JSON.parse(message.data);
	} catch (e) {
		data = message.data;
	}
	console.log("WS message:", data);

	if (data == "Server ready." && page == "analytics") {
		request_sensorsList();
		request_whole_temperature_data();
		request_whole_pressure_data();
		request_whole_illuminance_data();
	}
	if (data == "Server ready." && page == "home") {
		request_lightsList();
		request_sensorsState();
		request_sensorsList();
		request_webWeatherOWM();
		request_sensors_measure_now();
	}
	sendToServer("Hi from browser. Got your message.");

	if (data["message"] == "sensorsList") {
		sensorsList = Object.assign({}, data["reply"]);
		sensorsListFull = Object.assign({}, data["reply"]);
		if (page == "analytics") {
			drawSensorsList(sensorsList);
		}
	}
	if (data["passport"] == "communication") {
		displayInDivEventLog(data);
	}
	if (data["message"] == "whole_temperature_data") {
		dataTemperatureFull = data["reply"];
	}
	if (data["message"] == "whole_pressure_data") {
		dataPressureFull = data["reply"];
	}
	if (data["message"] == "whole_illuminance_data") {
		dataIlluminanceFull = data["reply"];
	}
	if (data["message"] == "webWeatherOWM") {
		webWeatherOWM = data["reply"];

		if (!jQuery.isEmptyObject(webWeatherOWM)) {
			drawWebWeatherOWM();
		}
	}
	if (data["message"] == "lightsList") {
		lightsList = data["reply"];
		drawLightsState();
	}
	// drawLightsList()
	if (data["message"] == "sensorsState") {
		sensorsState = data["reply"];
		if (!jQuery.isEmptyObject(sensorsState)) {
			drawSensorsState();
		}
	}
	if (data["message"] == "sensorsState" || data["message"] == "sensorsList") {
		if (
			page == "home" &&
			!jQuery.isEmptyObject(sensorsListFull) && //if is home and sensorsListFull && sensorsState already came
			!jQuery.isEmptyObject(sensorsState)
		) {
			drawCurrentlyMeasuredValue();
		}
	}
	if (data["message"] == "controller") {
		controller_state = data;
		drawControllersState();
	}
}

function drawLightsState() {
	$("#light_container").empty();
	for (const [key, value] of Object.entries(lightsList)) {
		for (var light in value) {
			if ("state" in value[light]) {
				if (value[light]["state"] == 1) {
					$("#light_container").append(
						$("<div/>").append(
							$("<img></img>")
								.attr("src", "/img/light/lightbulbon.svg")
								.attr("alt", "lightbulbon")
								.attr("class", "light_bulb")
								.attr("light_ID", value[light]["ID"])
								.attr("type", key.toString())
								.attr("id", key.toString() + value[light]["ID"].toString())
								.click(function () {
									console.log($(this));
									request_lightCommand(
										$(this).attr("type"),
										parseInt($(this).attr("light_ID")),
										0
									);
								}),
							$("<span></span>").text(
								// "key = " + key + " id = " + value[light]["ID"]
								value[light]["description"]
							)
						)
					);
				}
				if (value[light]["state"] == 0) {
					$("#light_container").append(
						$("<div/>").append(
							$("<img></img>")
								.attr("src", "/img/light/lightbulboff.svg")
								.attr("alt", "lightbulboff")
								.attr("class", "light_bulb")
								.attr("light_ID", value[light]["ID"])
								.attr("type", key.toString())
								.attr("id", key.toString() + value[light]["ID"].toString())
								.click(function () {
									console.log($(this));
									request_lightCommand(
										$(this).attr("type"),
										parseInt($(this).attr("light_ID")),
										1
									);
								}),
							$("<span></span>").text(value[light]["description"])
						)
					);
				}
			} else {
				$("#light_container").append(
					$("<div/>").append(
						$("<img></img>")
							.attr("src", "/img/light/lightbulbunenable.svg")
							.attr("alt", "lightbulbunenable")
							.attr("class", "light_bulb")
							.attr("ID", value[light]["ID"])
							.attr("type", key.toString())
							.attr("id", key.toString() + value[light]["ID"].toString())
							.click(function () {
								console.log($(this));
							}),
						$("<span></span>").text(value[light]["description"])
					)
				);
			}
		}
	}
}

function toggleFilter(element) {
	let key = element.getAttribute("key");
	let value = element.getAttribute("room");
	if (element.checked) {
		let element = sensorsListFull[key].find((element) => element.room == value);
		sensorsList[key].push(element);
	} else {
		sensorsList[key] = sensorsList[key].filter((item) => item.room !== value);
	}
}

function drawWebWeatherOWM() {
	webWeatherOWM;
	let unix_timestamp = webWeatherOWM.current_time;
	// Create a new JavaScript Date object based on the timestamp
	// multiplied by 1000 so that the argument is in milliseconds, not seconds.
	date = new Date(unix_timestamp * 1000);
	date_dd = String(date.getDate()).padStart(2, "0");
	date_mm = String(date.getMonth() + 1).padStart(2, "0"); //January is 0!
	date_yyyy = date.getFullYear();

	date_full_date = date_dd + "/" + date_mm + "/" + date_yyyy;

	if (date.getHours() < 10) {
		data_full_hours = "0" + date.getHours().toString();
	} else {
		data_full_hours = date.getHours().toString();
	}

	if (date.getMinutes() < 10) {
		data_full_minutes = "0" + date.getMinutes().toString();
	} else {
		data_full_minutes = date.getMinutes().toString();
	}

	$("#time").empty();
	$("#time").append(
		$("<span></span>").text(date_full_date),
		$("</br>"),
		$("<span></span>").text(data_full_hours + ":" + data_full_minutes)
	);
	$("#today").empty();
	$("#today").append(
		$("<span></span>").text("Today"),
		$("</br>"),
		$("<img/>")
			.attr("style", "width: 3em; height: 3em")
			.attr("src", "/img/weather/" + webWeatherOWM.today_icon + ".svg")
			.attr("alt", "icon " + webWeatherOWM.today_icon),
		$("<span></span>").text(
			(Math.round(webWeatherOWM.current_temperature * 10) / 10).toString() +
				"°C"
		),
		$("</br>"),
		$("<span></span>").text(
			(Math.round(webWeatherOWM.today_temperature_day * 10) / 10).toString() +
				"°C/" +
				(
					Math.round(webWeatherOWM.today_temperature_night * 10) / 10
				).toString() +
				"°C"
		),
		$(
			'<img class="umbrella" id="today" src="/img/weather/umbrella.svg" alt="umbrella"/>'
		),
		$("<span></span>").text(webWeatherOWM.today_rain + "mm/h")
	);
	$("#tomorrow").empty();
	$("#tomorrow").append(
		$("<span></span>").text("Tomorrow"),
		$("</br>"),
		$("<img/>")
			.attr("style", "width: 1.7em; height: 1.7 em")
			.attr("src", "/img/weather/" + webWeatherOWM.tomorrow_icon + ".svg")
			.attr("alt", webWeatherOWM.tomorrow_icon),
		$("<span></span>").text(
			(
				Math.round(webWeatherOWM.tomorrow_temperature_day * 10) / 10
			).toString() +
				"°C/" +
				(
					Math.round(webWeatherOWM.tomorrow_temperature_night * 10) / 10
				).toString() +
				"°C"
		),
		$(
			'<img class="umbrella" id = "tomorrow" src="/img/weather/umbrella.svg" alt="umbrella"/>'
		),
		$("<span></span>").text(webWeatherOWM.tomorrow_rain + "mm/h")
	);
}

function drawCurrentlyMeasuredValue() {
	$("#measured_value_container").empty();
	rooms = [];
	console.log("drawCurrentlyMeasuredValue");

	// for (const [key, value] of Object.entries(sensorsState)) {
	for (const [sensor_type, sensor_list_of_type] of Object.entries(
		sensorsState
	)) {
		sensor_list_of_type.forEach((sensor_value) => {
			if (rooms.includes(sensor_value.room) == false) {
				rooms.push(sensor_value.room);
				$("#measured_value_container").append(
					$("<div/>")
						.addClass("sensors row measured_value room_title")

						.attr("id", sensor_value.room),
					$("<div/>")
						.addClass("sensors row measured_value room_body")

						.attr("id", sensor_value.room)
				);
				$(".sensors.row.measured_value.room_title#" + sensor_value.room).append(
					$("<span></span>")
						.addClass("sensors room measured_value")
						.text(sensor_value.room_description)
				);
			}
			$(".sensors.row.measured_value.room_body#" + sensor_value.room).append(
				$("<div/>")
					.addClass("measured_values_item card border-2 col-auto")
					.append(
						$("<span></span>")
							.addClass("card-title text-center text-wrap title measured_value")
							.text(sensor_value.description),
						$("<div/>")
							.addClass("card-body text-center sensors measured_value")
							.attr("id", sensor_value.sensor_id + " " + sensor_value.room)
							.append(
								$("<span></span").text(
									Math.round(sensor_value.value * 10) / 10
								),
								$("<img/>")
									.addClass("sensors measured_value")
									.attr("src", "/img/quantity/" + sensor_type + ".svg")
									.attr("alt", sensor_type)
							)
					)
			);
		});
	}
}

// call drawSensorsState every 10 min
var drawSensorsState_intervalId = window.setInterval(function () {
	drawSensorsState();
}, 600000);

function drawSensorsState() {
	$("#sensors_container").empty();
	$.each(sensorsState, function (sensor_type, sensor_list_of_type) {
		sensor_list_of_type.forEach((sensor_value) => {
			valDate = new Date(sensor_value.timestamp);
			now = new Date();
			const diffTime = Math.abs(now - valDate);
			if (diffTime > 300000) {
				//longer then 5 min
				$("#sensors_container").append(
					'<div><i style="color: red" class="bi bi-dash-circle-fill sensor_state_icon"></i><span>' +
						sensor_value.description +
						+"</span><span> <b> Sensor did not responded for more than 5 minutes </b> </span></div>"
				);
				return;
			}
			if (sensor_value["state"] == "ok") {
				$("#sensors_container").append(
					'<div><i style="color: green" class="bi bi-check-circle-fill sensor_state_icon"></i> <span> ' +
						sensor_value.description +
						" </span></div>"
				);
				return;
			} else {
				$("#sensors_container").append(
					'<div><i style="color: red" class="bi bi-dash-circle-fill sensor_state_icon"></i> <span> ' +
						sensor_value.description +
						"</span></div>"
				);
				return;
			}
		});
	});
}

function drawSensorsList(data) {
	console.log("drawSensorsList");
	filterDiv = document.getElementById("filter-container");
	$("#filter-container")
		.empty()
		.append($("<h2/>").text("Nastavaní pro vykreslení dat"));
	console.log(data);
	// Object.keys(data).forEach((key) => {
	for (const [key, value] of Object.entries(data)) {
		if (typeof value == "undefined") {
			return;
		}
		if (key == "max_room") {
			MAXROOM = value;
		} else {
			let keyFilterDiv = document.createElement("div");
			keyFilterDiv.className = "form-group";
			keyFilterDiv.id = key;
			filterDiv.appendChild(keyFilterDiv);

			let titleFilter = document.createElement("h4");
			titleFilter.innerHTML = key[0].toUpperCase() + key.slice(1);
			keyFilterDiv.appendChild(titleFilter);

			value.forEach((element) => {
				elementFilterDiv = document.createElement("div");
				elementFilterDiv.id = element.room + key + "Div";
				elementFilterDiv.className = "custom-control custom-switch";
				keyFilterDiv.appendChild(elementFilterDiv);

				elementFilterCheckbox = document.createElement("input");
				elementFilterCheckbox.className = "custom-control-input";
				elementFilterCheckbox.type = "checkbox";

				// elementFilterCheckbox.setAttribute("value", "");
				elementFilterCheckbox.id = element.room + key + "Checkbox";
				elementFilterCheckbox.setAttribute("key", key);
				elementFilterCheckbox.setAttribute("room", element.room);
				elementFilterCheckbox.setAttribute("onclick", "toggleFilter(this)");
				elementFilterCheckbox.checked = true;
				elementFilterDiv.appendChild(elementFilterCheckbox);

				elementFilterLabel = document.createElement("label");
				elementFilterLabel.className = "custom-control-label";
				elementFilterLabel.id = element.room + key + "Label";
				elementFilterLabel.setAttribute("for", element.room + key + "Checkbox");
				elementFilterLabel.innerHTML = element.description;
				elementFilterDiv.appendChild(elementFilterLabel);
			});
		}
	}
	filterDiv.insertAdjacentHTML(
		"beforeend",
		`<button type="submit" class="btn btn-primary" onclick="drawGraphs()" >Vykreslit data</button>`
	);
}

function restructureTemperatureData() {
	data = dataTemperatureFull;
	console.log("restructureTemperatureData");
	dataTemperature = "";
	pattern = /^(room_)\d+$/gm;

	data.forEach((element) => {
		loc = element.location;
		if (element.state == "error") {
			return;
		}
		if (sensorsList.temperature.some((e) => element.location === e.room)) {
			loc = parseInt(loc.replace("room_", ""));
			dataTemperature =
				dataTemperature +
				(element.timestamp.replace("-", "/") +
					",".repeat(loc) +
					element.temperature_value.toString() +
					",".repeat(MAXROOM - loc) +
					"\n");
		}
	});
}

function restructureIlluminanceData() {
	data = dataIlluminanceFull;
	console.log("restructureIlluminanceData");
	dataIlluminance = "";
	pattern = /^(room_)\d+$/gm;

	data.forEach((element) => {
		loc = element.location;
		if (element.state == "error") {
			return;
		}
		if (sensorsList.illuminance.some((e) => element.location === e.room)) {
			loc = parseInt(loc.replace("room_", ""));
			dataIlluminance =
				dataIlluminance +
				(element.timestamp.replace("-", "/") +
					",".repeat(loc) +
					element.illuminance_value.toString() +
					",".repeat(MAXROOM - loc) +
					"\n");
		}
	});
}

function restructurePressureData() {
	data = dataPressureFull;
	console.log("restructurePressureData");
	dataPressure = "";
	pattern = /^(room_)\d+$/gm;

	data.forEach((element) => {
		loc = element.location;
		if (element.state == "error") {
			return;
		}
		if (sensorsList.pressure.some((e) => element.location === e.room)) {
			loc = parseInt(loc.replace("room_", ""));
			dataPressure =
				dataPressure +
				(element.timestamp.replace("-", "/") +
					",".repeat(loc) +
					element.pressure_value.toString() +
					",".repeat(MAXROOM - loc) +
					"\n");
		}
	});
}

function drawGraphs() {
	graphContainer = document.getElementById("graph-confainer");
	graphContainer.innerHTML = "";
	if (
		dataTemperatureFull.length == 0 ||
		dataPressureFull.length == 0 ||
		dataIlluminanceFull.length == 0
	) {
		alert(
			"Data from server are still not fully downloaded. Please try again in a moment."
		);
	} else {
		drawTemperatureGraph();
		drawPressureGraph();
		drawIlluminanceGraph();
	}
}

function drawIlluminanceGraph() {
	restructureIlluminanceData();
	if (dataIlluminance.length == 0) return 0;
	let graph = document.createElement("div");
	graph.className = "dyGraphs";
	graphContainer.appendChild(graph);
	var g = new Dygraph(graph, dataIlluminance, {
		labels: ["Time", "Illuminance value room_1", "Illuminance value room_2"],
		// height: 320,
		// width: 480,
		rollPeriod: 1,
		showRoller: true,
		title: "Illuminance data",
		legend: "always",
		// stackedGraph: true,
		// highlightCircleSize: 2,
		// strokeWidth: 1,
		// strokeBorderWidth: null,
		// highlightSeriesOpts: {
		// 	strokeWidth: 3,
		// 	strokeBorderWidth: 1,
		// 	highlightCircleSize: 5,
		// },
		showRangeSelector: true,
		rangeSelectorHeight: 30,
		// dateWindow: [
		// 	new Date("2020-12-05 00:00:00"),
		// 	new Date("2020-12-05 12:00:00"),
		// ],
	});
}

function drawTemperatureGraph() {
	restructureTemperatureData();
	if (dataTemperature.length == 0) return 0;
	let graph = document.createElement("div");
	graph.className = "dyGraphs";
	graphContainer.appendChild(graph);
	var g = new Dygraph(graph, dataTemperature, {
		labels: ["Time", "Temperature value room_1", "Temperature value room_2"],
		// height: 320,
		// width: 480,
		rollPeriod: 1,
		showRoller: true,
		title: "Temperature data",
		legend: "always",
		// stackedGraph: true,
		// highlightCircleSize: 2,
		// strokeWidth: 1,
		// strokeBorderWidth: null,
		// highlightSeriesOpts: {
		// 	strokeWidth: 3,
		// 	strokeBorderWidth: 1,
		// 	highlightCircleSize: 5,
		// },
		showRangeSelector: true,
		rangeSelectorHeight: 30,
		// dateWindow: [
		// 	new Date("2020-12-05 00:00:00"),
		// 	new Date("2020-12-05 12:00:00"),
		// ],
	});
}

function drawPressureGraph() {
	restructurePressureData();
	if (dataPressure.length == 0) return 0;
	let graph = document.createElement("div");
	graph.className = "dyGraphs";
	graphContainer.appendChild(graph);
	var g = new Dygraph(graph, dataPressure, {
		labels: ["Time", "Pressure value room_1", "Pressure value room_2"],
		// height: 320,
		// width: 480,
		rollPeriod: 1,
		showRoller: true,
		title: "Pressure data",
		legend: "always",
		// stackedGraph: true,
		// highlightCircleSize: 2,
		// strokeWidth: 1,
		// strokeBorderWidth: null,
		// highlightSeriesOpts: {
		// 	strokeWidth: 3,
		// 	strokeBorderWidth: 1,
		// 	highlightCircleSize: 5,
		// },
		showRangeSelector: true,
		rangeSelectorHeight: 30,
		// dateWindow: [
		// 	new Date("2020-12-05 00:00:00"),
		// 	new Date("2020-12-05 12:00:00"),
		// ],
	});
}

function displayInDivEventLog(data) {
	var today = new Date();
	var time =
		(today.getHours() < 10 ? "0" : "") +
		today.getHours() +
		":" +
		(today.getMinutes() < 10 ? "0" : "") +
		today.getMinutes() +
		":" +
		(today.getSeconds() < 10 ? "0" : "") +
		today.getSeconds();

	let divEventLog = document.getElementById("eventLog");
	if (divEventLog.childNodes.length >= 5) {
		divEventLog.removeChild(divEventLog.lastChild);
	}

	let eventLogItem = document.createElement("div");
	eventLogItem.id = "eventLogItem";
	eventLogItem.className = "alert alert-info";
	eventLogItem.innerHTML =
		time + " <strong>" + data.source + "</strong> => " + data.message;
	divEventLog.prepend(eventLogItem);
}

function onSocketClose() {
	console.log("WS client: Websocket closed.");
}

function request_whole_temperature_data() {
	msg = "whole_temperature_data";
	sendToServer(msg, "sensors");
}

function request_sensors_measure_now() {
	msg = "sensors_measure_now";
	sendToServer(msg, "sensors");
}

function request_whole_pressure_data() {
	msg = "whole_pressure_data";
	sendToServer(msg, "sensors");
}

function request_sensorsState() {
	msg = "sensorsState";
	sendToServer(msg, "sensors");
}

function request_whole_illuminance_data() {
	msg = "whole_illuminance_data";
	sendToServer(msg, "sensors");
}

function request_sensorsList() {
	msg = "sensorsList";
	sendToServer(msg, "sensors");
}

function request_lightsList() {
	msg = "lightsList";
	sendToServer(msg, "lights/state");
}

function request_lightCommand(type, id, set) {
	second_param = {
		ID: id,
		type: type,
		set: set,
	};
	msg = "lightCommand";
	sendToServer(msg, "lights/state", second_param);
}

function request_webWeatherOWM() {
	msg = "webWeatherOWM";
	sendToServer(msg, "weather");
}

function sendToServer(message, passport = "", second_param = "") {
	let payload = {
		passport: passport,
		message: message,
		second_param: second_param,
	};
	ws.send(JSON.stringify(payload));
}

function loadJsonHandler() {
	let xmlhttp;
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}
	xmlhttp.open("GET", "/packet", false);
	xmlhttp.send(null);

	return JSON.parse(xmlhttp.responseText);
}

function getModules() {
	return loadJsonHandler().modules;
}

function getModules_off() {
	return loadJsonHandler().modules_off;
}

function fillModules() {
	console.log("Loading modules");
	let modules = getModules();
	let modules_off = getModules_off();

	let divModules = document.getElementById("modules");
	let moduleList = document.createElement("ul");
	moduleList.className = "list-group sticky-top-4";
	divModules.appendChild(moduleList);

	for (let i_module = 0; i_module < modules.length; i_module++) {
		// fill in table of modules with toggles
		drawModule(moduleList, modules[i_module], true);
	}
	for (let i_module = 0; i_module < modules_off.length; i_module++) {
		// fill in table of modules with toggles
		drawModule(moduleList, modules_off[i_module], false);
	}
}

function drawModule(moduleList, module, checked) {
	let divModulesInformation = document.getElementById("modules_information");

	let moduleListItem = document.createElement("li");
	moduleListItem.className =
		"list-group-item d-flex justify-content-between align-items-center";
	moduleListItem.id = module.module_id + "Li";
	moduleList.appendChild(moduleListItem);

	let moduleTitle = document.createElement("h5");
	moduleTitle.innerHTML = module.module_id;
	moduleListItem.appendChild(moduleTitle);

	let moduleSpanToggle = document.createElement("div");
	moduleSpanToggle.className = "checkbox";
	moduleListItem.appendChild(moduleSpanToggle);

	let moduleToggle = document.createElement("input");
	moduleToggle.type = "checkbox";
	moduleToggle.id = module.module_id;

	moduleToggle.checked = checked;
	moduleToggle.setAttribute("data-toggle", "toggle");
	moduleToggle.setAttribute("data-size", "sm");
	moduleSpanToggle.appendChild(moduleToggle);

	//init of bootstrap toogles
	// "#".concat(module.module_id);
	$(moduleToggle).bootstrapToggle();

	$(function () {
		$(moduleToggle).change(function () {
			turnModuleOnOff($(this).prop("checked"), $(this).attr("id"));
		});
	});

	let moduleDiv = document.createElement("DIV");
	moduleDiv.id = module.module_id + "Div";
	moduleDiv.className = "d-none";

	let moduleHeaderDiv = document.createElement("div");
	moduleHeaderDiv.className = "custom-card-header sticky-top-4";
	moduleDiv.appendChild(moduleHeaderDiv);

	let moduleTitleDiv = document.createElement("h5");
	moduleTitleDiv.className = "card-desk-title";
	moduleTitleDiv.innerHTML = module.module_id;
	moduleHeaderDiv.appendChild(moduleTitleDiv);

	let moduleDescriptionDiv = document.createElement("p");
	moduleDescriptionDiv.className = "card-desk-description";
	moduleDescriptionDiv.innerHTML = module.description;
	moduleHeaderDiv.appendChild(moduleDescriptionDiv);

	let moduleMovesDiv = document.createElement("DIV");
	moduleMovesDiv.className =
		"module_moves d-flex flex-row flex-wrap justify-content-start";
	moduleDiv.appendChild(moduleMovesDiv);

	$("#" + module.module_id + "Li").click(function () {
		if (typeof $lastToggledModuleId !== "undefined") {
			$($lastToggledModuleId).toggleClass("d-none");
			$lastToggledModuleId = "#" + module.module_id + "Div";
			$($lastToggledModuleId).toggleClass("d-none");
		} else {
			$lastToggledModuleId = "#" + module.module_id + "Div";
			$("#" + module.module_id + "Div").toggleClass("d-none");
		}
	});

	divModulesInformation.appendChild(moduleDiv);

	for (let i_move = 0; i_move < module.moves.length; i_move++) {
		let moveDiv = document.createElement("DIV");
		moveDiv.className = "card m-3";

		let moveDivBody = document.createElement("DIV");
		moveDivBody.className = "card-body";
		moveDiv.appendChild(moveDivBody);

		let moveTitleDiv = document.createElement("h5");
		moveTitleDiv.className = "card-title";
		moveTitleDiv.innerHTML = module.moves[i_move].method_name;
		moveDivBody.appendChild(moveTitleDiv);

		let moveDescriptionDiv = document.createElement("span");
		moveDescriptionDiv.className = "card-text";
		moveDescriptionDiv.innerHTML = module.moves[i_move].description;
		moveDivBody.appendChild(moveDescriptionDiv);

		let moveCallsDiv = document.createElement("DIV");
		moveCallsDiv.className = "move_calls";
		moveDivBody.appendChild(moveCallsDiv);

		moduleMovesDiv.appendChild(moveDiv);

		for (let i_call = 0; i_call < module.moves[i_move].calls.length; i_call++) {
			let moveCallDiv = document.createElement("span");
			moveCallDiv.className = "badge badge-pill badge-primary m-1";
			moveCallDiv.innerHTML = module.moves[i_move].calls[i_call]
				.toString()
				.replace(",", " ");
			moveCallsDiv.appendChild(moveCallDiv);
		}
	}
}
