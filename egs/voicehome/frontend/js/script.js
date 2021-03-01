// Global variables
// var dataTemperature = [];
var sensorsListFull = [];
var dataTemperatureFull = [];
var dataTemperature = "";
var dataPressureFull = [];
var dataPressure = "";
var dataIlluminanceFull = [];
var dataIlluminance = "";
var MAXROOM;
var page = "home";

// var ws_address = "ws://147.228.124.230:8881/websocket";
var ws_address = "ws://127.0.0.1:8881/websocket";

function onBodyLoadModules() {
	page = "modules";
	console.log("Web GUI loaded.");
	ws = new WebSocket(ws_address); // ws is a global variable (index.html)
	ws.onopen = onSocketOpen;
	ws.onmessage = onSocketMessage;
	ws.onclose = onSocketClose;

	console.log("Controller:", get_controller_id());

	fillModules();
}

function onBodyLoad() {
	page = "home";
	console.log("Web GUI loaded.");
	ws = new WebSocket(ws_address); // ws is a global variable (index.html)
	ws.onopen = onSocketOpen;
	ws.onmessage = onSocketMessage;
	ws.onclose = onSocketClose;

	console.log("Controller:", get_controller_id());
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

	// request_sensorsList();
	// request_whole_temperature_data();
	// request_sensorsList();
	// request_whole_temperature_data();
	// request_whole_pressure_data();
}

function onSocketOpen() {
	console.log("WS client: Websocket opened.");
}

function onSocketMessage(message) {
	let data;
	try {
		data = JSON.parse(message.data);
	} catch (e) {
		data = message.data;
	}
	if (
		data.constructor === {}.constructor &&
		(data.source == "keyboard" || data.source == "engine")
	) {
		displayInDivEventLog(data);
	}
	console.log("WS message:", data);

	if (data == "Server ready." && page == "analytics") {
		request_sensorsList();
		request_whole_temperature_data();
		request_whole_pressure_data();
		request_whole_illuminance_data();
	}
	sendToServer("Hi from browser. Got your message.");
	switch (data["message"]) {
		case "sensorsList":
			console.log(data["reply"]);
			sensorsList = Object.assign({}, data["reply"]);
			sensorsListFull = Object.assign({}, data["reply"]);
			drawSensorsList(sensorsList);
			break;
		case "whole_temperature_data":
			dataTemperatureFull = data["reply"];
			break;
		case "whole_pressure_data":
			dataPressureFull = data["reply"];
			break;
		case "whole_illuminance_data":
			dataIlluminanceFull = data["reply"];
			// console.log("dataIlluminanceFull=");
			// console.log(dataIlluminanceFull);
			break;

			otherwise: console.log("pass on onSocketMessage");
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

function drawSensorsList(data) {
	console.log("drawSensorsList");
	filterDiv = document.getElementById("filter-container");
	filterDiv.innerHTML = "";
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

			let titleFilter = document.createElement("h3");
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
				elementFilterLabel.innerHTML = element.room;
				elementFilterDiv.appendChild(elementFilterLabel);
			});
		}
	}
	filterDiv.insertAdjacentHTML(
		"beforeend",
		`<button type="submit" class="btn btn-primary" onclick="drawGraphs()" >Submit</button>`
	);
}

// function restructureTemperatureData() {
// 	data = dataTemperatureFull;
// 	dataTemperature = [];
// 	console.log("restructureTemperatureData");
// 	console.log(data);
// 	data.forEach((element) => {
// 		if (
// 			element.temperature_value < 100 &&
// 			sensorsList.temperature.some((e) => element.location === e.room)
// 		) {
// 			switch (element.location) {
// 				case "room_1":
// 					dataElement =
// 						new Date(element.timestamp).toString() +
// 						"," +
// 						element.temperature_value.toString() +
// 						",\n";
// 					dataTemperature += dataElement;
// 					break;

// 				case "room_2":
// 					dataElement =
// 						new Date(element.timestamp).toString() +
// 						",," +
// 						element.temperature_value.toString() +
// 						"\n";
// 					dataTemperature += dataElement;
// 					break;
// 				default:
// 					break;
// 			}
// 		}
// 	});
// }

function restructureTemperatureData() {
	data = dataTemperatureFull;
	console.log("restructureTemperatureData");
	dataTemperature = "";
	pattern = /^(room_)\d+$/gm;

	data.forEach((element) => {
		loc = element.location;
		if (element.status == "error") {
			return;
		}
		// if (pattern.test(loc) == false) {
		// 	return;
		// }
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
		if (element.status == "error") {
			return;
		}
		// if (pattern.test(loc) == false) {
		// 	return;
		// }
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
		if (element.status == "error") {
			return;
		}
		// if (pattern.test(loc) == false) {
		// 	return;
		// }
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

// function restructurePressureData() {
// 	data = dataPressureFull;
// 	dataPressure = [];
// 	console.log("restructureTemperatureData");
// 	console.log(data);
// 	data.forEach((element) => {
// 		if (
// 			1 < element.pressure_value &&
// 			element.pressure_value < 5000 &&
// 			sensorsList.pressure.some((e) => element.location === e.room)
// 		) {
// 			switch (element.location) {
// 				case "room_1":
// 					dataElement =
// 						new Date(element.timestamp).toString() +
// 						"," +
// 						element.pressure_value.toString() +
// 						",\n";
// 					dataPressure += dataElement;
// 					break;

// 				case "room_2":
// 					dataElement =
// 						new Date(element.timestamp).toString() +
// 						",," +
// 						element.pressure_value.toString() +
// 						"\n";
// 					dataPressure += dataElement;
// 					break;
// 				default:
// 					break;
// 			}
// 		}
// 	});
// }

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
	// console.log("dataIlluminance=");
	// console.log(dataIlluminance);
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
	// console.log("dataTemperature = ");
	// console.log(dataTemperature);
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
	// console.log("dataPressure= ");
	// console.log(dataPressure);
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
		today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();

	let divEventLog = document.getElementById("eventLog");
	if (divEventLog.childNodes.length >= 5) {
		divEventLog.removeChild(divEventLog.firstChild);
	}

	let eventLogItem = document.createElement("div");
	eventLogItem.id = "eventLogItem";
	eventLogItem.className = "alert alert-info";
	eventLogItem.innerHTML =
		time + " <strong>" + data.source + "</strong> => " + data.message;
	divEventLog.appendChild(eventLogItem);
}

function onSocketClose() {
	console.log("WS client: Websocket closed.");
}

function request_whole_temperature_data() {
	msg = "whole_temperature_data";
	sendToServer(msg, "voicehome/sensors");
}

function request_whole_pressure_data() {
	msg = "whole_pressure_data";
	sendToServer(msg, "voicehome/sensors");
}

function request_whole_illuminance_data() {
	msg = "whole_illuminance_data";
	sendToServer(msg, "voicehome/sensors");
}

function request_sensorsList() {
	msg = "sensorsList";
	sendToServer(msg, "voicehome/sensors");
}

function sendToServer(message, passport = "") {
	let payload = {
		passport: passport,
		message: message,
		second_param: [1, 2],
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

function fillModules() {
	console.log("Loading modules");
	let modules = loadJsonHandler().modules;
	let modules_off = loadJsonHandler().modules_off;

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
	// moduleDiv.className = "overflow-scroll";
	// moduleDiv.style.overflowY = "scroll";

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
			// console.log($lastToggledModuleId);
		} else {
			$lastToggledModuleId = "#" + module.module_id + "Div";
			$("#" + module.module_id + "Div").toggleClass("d-none");
			// console.log($lastToggledModuleId);
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
