$(document).ready(function () {
	var data = [];
	var t = new Date();
	for (var i = 1000; i >= 0; i--) {
		var x = new Date(t.getTime() - i * 1000);
		data.push([x, Math.random()]);
	}

	var g = new Dygraph(document.getElementById("div_g"), data, {
		rollPeriod: 1,
		showRoller: true,
		// customBars: true,
		title: "Daily Temperatures in New York vs. San Francisco",
		legend: "always",
		showRangeSelector: true,
		rangeSelectorHeight: 30,
		labels: ["Time", "Temperature value"],
	});
	// It sucks that these things aren't objects, and we need to store state in window.
	window.intervalId = setInterval(function () {
		var x = new Date(); // current time
		var y = Math.random();
		data.push([x, y]);
		g.updateOptions({
			file: data,
		});
	}, 3000);
});
