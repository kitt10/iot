function onBodyLoad() {
	console.log("Web GUI loaded.");
	ws = new WebSocket("ws://147.228.124.230:8881/websocket"); // ws is a global variable (index.html)
	// ws = new WebSocket("ws://127.0.0.1:8881/websocket"); // ws is a global variable (index.html)
	ws.onopen = onSocketOpen;
	ws.onmessage = onSocketMessage;
	ws.onclose = onSocketClose;

	fillModules();
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

function testData() {
	msg = {'message': 'ahoj',
		'day_average': 21
	}
	sendToServer(msg, 'voicehome/sensors')
}

function sendToServer(message, passport='') {
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

		// fill in modules information
		// let divModulesInformationItem = document.createElement("div");
		// divModulesInformation.appendChild(divModulesInformationItem);

		// for more information of module uncomment following

		//  let moduleDescriptionDiv = document.createElement("DIV");
		// moduleDescriptionDiv.className = "module_description";
		// moduleDescriptionDiv.innerHTML = modules[i_module].description;
		// moduleList.appendChild(moduleDescriptionDiv);

		// let moduleMovesDiv = document.createElement("DIV");
		// moduleMovesDiv.className = "module_moves";
		// moduleList.appendChild(moduleMovesDiv);

		// divModules.appendChild(moduleList);

		// for (let i_move = 0; i_move < modules[i_module].moves.length; i_move++) {
		// 	let moveDiv = document.createElement("DIV");
		// 	moveDiv.className = "move";

		// 	let moveTitleDiv = document.createElement("DIV");
		// 	moveTitleDiv.className = "move_title";
		// 	moveTitleDiv.innerHTML = modules[i_module].moves[i_move].method_name;
		// 	moveDiv.appendChild(moveTitleDiv);

		// 	let moveDescriptionDiv = document.createElement("DIV");
		// 	moveDescriptionDiv.className = "move_description";
		// 	moveDescriptionDiv.innerHTML =
		// 		modules[i_module].moves[i_move].description;
		// 	moveDiv.appendChild(moveDescriptionDiv);

		// 	let moveCallsDiv = document.createElement("DIV");
		// 	moveCallsDiv.className = "move_calls";
		// 	moveDiv.appendChild(moveCallsDiv);

		// 	moduleMovesDiv.appendChild(moveDiv);

		// 	for (
		// 		let i_call = 0;
		// 		i_call < modules[i_module].moves[i_move].calls.length;
		// 		i_call++
		// 	) {
		// 		let moveCallDiv = document.createElement("DIV");
		// 		moveCallDiv.className = "move_call";
		// 		moveCallDiv.innerHTML = modules[i_module].moves[i_move].calls[i_call]
		// 			.toString()
		// 			.replace(",", " ");
		// 		moveCallsDiv.appendChild(moveCallDiv);
		// 	}
		// }
	}
}
