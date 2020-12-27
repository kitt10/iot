// Global variables
var temperatureData;

function onBodyLoad() {
	console.log("Web GUI loaded.");
	ws = new WebSocket("ws://147.228.124.230:8881/websocket"); // ws is a global variable (index.html)
	// ws = new WebSocket("ws://127.0.0.1:8881/websocket"); // ws is a global variable (index.html)
	ws.onopen = onSocketOpen;
	ws.onmessage = onSocketMessage;
	ws.onclose = onSocketClose;

	fillModules();
}

function onBodyLoadAnalytics() {
	console.log("onBodyLoadAnalytics");
	console.log("Web GUI loaded.");
	ws = new WebSocket("ws://147.228.124.230:8881/websocket"); // ws is a global variable (index.html)
	// ws = new WebSocket("ws://127.0.0.1:8881/websocket"); // ws is a global variable (index.html)
	ws.onopen = onSocketOpen;
	ws.onmessage = onSocketMessage;
	ws.onclose = onSocketClose;

	request_whole_temperature_data();
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
	if (data.constructor === {}.constructor && data.source == "keyboard") {
		displayInDivEventLog(data);
	}
	console.log("WS message:", data);
	console.log(typeof data);
	sendToServer("Hi from browser. Got your message.");
	switch (data["message"]) {
		case "whole_temperature_data":
			restructureTemperatureData(data);

			otherwise: console.log("pass on onSocketMessage");
	}
}

var chartJsData = function (resultSet) {
	return {
		datasets: [
			{
				label: "Temperature",
				data: resultSet,
				backgroundColor: "rgb(255, 99, 132)",
			},
		],
	};
};
var options = {
	scales: {
		xAxes: [
			{
				type: "time",
				time: {
					displayFormats: {
						hour: "YYYY-MM-DD HH:mm:ss",
					},
					tooltipFormat: "YYYY-MM-DD HH:mm:ss",
				},
			},
		],
		yAxes: [
			{
				ticks: {
					// beginAtZero: true,
				},
			},
		],
	},
};

function restructureTemperatureData(data) {
	data = data["reply"];
	data_temperature = [];
	console.log("restructureTemperatureData");
	console.log(data);
	data.forEach((element) => {
		if (element.temperature_value < 100) {
			switch (element.location) {
				case "room_1":
					dataElement =
						new Date(element.timestamp).toString() +
						"," +
						element.temperature_value.toString() +
						",\n";
					data_temperature += dataElement;
					break;

				case "room_2":
					dataElement =
						new Date(element.timestamp).toString() +
						",," +
						element.temperature_value.toString() +
						"\n";
					data_temperature += dataElement;
					break;
				default:
					break;
			}
		}
	});
	temperatureData = data_temperature;
}

function drawTemperatureGraph() {
	var g = new Dygraph(document.getElementById("div_g"), temperatureData, {
		rollPeriod: 1,
		showRoller: true,
		title: "Temperature data",
		legend: "always",
		showRangeSelector: true,
		rangeSelectorHeight: 30,
		labels: ["Time", "Temperature value room_1", "Temperature value room_2"],
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
	let divModules = document.getElementById("modules");
	let divModulesInformation = document.getElementById("modules_information");

	let moduleList = document.createElement("ul");
	moduleList.className = "list-group sticky-top-4";
	divModules.appendChild(moduleList);

	for (let i_module = 0; i_module < modules.length; i_module++) {
		// fill in table of modules with toggles
		let moduleListItem = document.createElement("li");
		moduleListItem.className =
			"list-group-item d-flex justify-content-between align-items-center";
		moduleListItem.id = modules[i_module].module_id + "Li";
		moduleList.appendChild(moduleListItem);

		let moduleTitle = document.createElement("h5");
		moduleTitle.innerHTML = modules[i_module].module_id;
		moduleListItem.appendChild(moduleTitle);

		let moduleSpanToggle = document.createElement("div");
		moduleSpanToggle.className = "checkbox";
		moduleListItem.appendChild(moduleSpanToggle);

		let moduleToggle = document.createElement("input");
		moduleToggle.type = "checkbox";
		moduleToggle.id = modules[i_module].module_id;
		moduleToggle.checked = true;
		moduleToggle.setAttribute("data-toggle", "toggle");
		moduleToggle.setAttribute("data-size", "sm");
		moduleSpanToggle.appendChild(moduleToggle);

		//init of bootstrap toogles
		$("#".concat(modules[i_module].module_id)).bootstrapToggle();

		let moduleDiv = document.createElement("DIV");
		moduleDiv.id = modules[i_module].module_id + "Div";
		moduleDiv.className = "d-none";
		// moduleDiv.className = "overflow-scroll";
		// moduleDiv.style.overflowY = "scroll";

		let moduleHeaderDiv = document.createElement("div");
		moduleHeaderDiv.className = "custom-card-header sticky-top-4";
		moduleDiv.appendChild(moduleHeaderDiv);

		let moduleTitleDiv = document.createElement("h5");
		moduleTitleDiv.className = "card-desk-title";
		moduleTitleDiv.innerHTML = modules[i_module].module_id;
		moduleHeaderDiv.appendChild(moduleTitleDiv);

		let moduleDescriptionDiv = document.createElement("p");
		moduleDescriptionDiv.className = "card-desk-description";
		moduleDescriptionDiv.innerHTML = modules[i_module].description;
		moduleHeaderDiv.appendChild(moduleDescriptionDiv);

		let moduleMovesDiv = document.createElement("DIV");
		moduleMovesDiv.className =
			"module_moves d-flex flex-row flex-wrap justify-content-start";
		moduleDiv.appendChild(moduleMovesDiv);

		$("#" + modules[i_module].module_id + "Li").click(function () {
			if (typeof $lastToggledModuleId !== "undefined") {
				$($lastToggledModuleId).toggleClass("d-none");
				$lastToggledModuleId = "#" + modules[i_module].module_id + "Div";
				$($lastToggledModuleId).toggleClass("d-none");
				console.log($lastToggledModuleId);
			} else {
				$lastToggledModuleId = "#" + modules[i_module].module_id + "Div";
				$("#" + modules[i_module].module_id + "Div").toggleClass("d-none");
				console.log($lastToggledModuleId);
			}
		});

		divModulesInformation.appendChild(moduleDiv);

		for (let i_move = 0; i_move < modules[i_module].moves.length; i_move++) {
			let moveDiv = document.createElement("DIV");
			moveDiv.className = "card m-3";

			let moveDivBody = document.createElement("DIV");
			moveDivBody.className = "card-body";
			moveDiv.appendChild(moveDivBody);

			let moveTitleDiv = document.createElement("h5");
			moveTitleDiv.className = "card-title";
			moveTitleDiv.innerHTML = modules[i_module].moves[i_move].method_name;
			moveDivBody.appendChild(moveTitleDiv);

			let moveDescriptionDiv = document.createElement("span");
			moveDescriptionDiv.className = "card-text";
			moveDescriptionDiv.innerHTML =
				modules[i_module].moves[i_move].description;
			moveDivBody.appendChild(moveDescriptionDiv);

			let moveCallsDiv = document.createElement("DIV");
			moveCallsDiv.className = "move_calls";
			moveDivBody.appendChild(moveCallsDiv);

			moduleMovesDiv.appendChild(moveDiv);

			for (
				let i_call = 0;
				i_call < modules[i_module].moves[i_move].calls.length;
				i_call++
			) {
				let moveCallDiv = document.createElement("span");
				moveCallDiv.className = "badge badge-pill badge-primary m-1";
				moveCallDiv.innerHTML = modules[i_module].moves[i_move].calls[i_call]
					.toString()
					.replace(",", " ");
				moveCallsDiv.appendChild(moveCallDiv);
			}
		}
	}
}
