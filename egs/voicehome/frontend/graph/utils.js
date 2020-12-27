$(document).ready(function () {
	var data = [];
	var data1 = [];
	var t = new Date();
	for (var i = 1000; i >= 0; i--) {
		var x = new Date(t.getTime() - i * 1000);
		data.push([x, Math.random()]);
	}
	for (var i = 1000; i >= 0; i--) {
		var x = new Date(t.getTime() - i * 1000);
		data1.push([x, Math.random()]);
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
			file: [data, data1],
		});
	}, 3000);
});

var data = [];
for (var i = 1; i <= 100; i++) {
	var m = "01",
		d = i;
	if (d > 31) {
		m = "02";
		d -= 31;
	}
	if (m == "02" && d > 28) {
		m = "03";
		d -= 28;
	}
	if (m == "03" && d > 31) {
		m = "04";
		d -= 31;
	}
	if (d < 10) d = "0" + d;
	// two series, one with range 1-100, one with range 1-2M
	data.push([
		new Date("2010/" + m + "/" + d),
		i,
		100 - i,
		1e6 * (1 + (i * (100 - i)) / (50 * 50)),
		1e6 * (2 - (i * (100 - i)) / (50 * 50)),
	]);
}

g = new Dygraph(document.getElementById("demodiv"), data, {
	labels: ["Date", "Y1", "Y2", "Y3", "Y4"],
	series: {
		Y3: { axis: "y2" },
		Y4: { axis: "y2" },
	},
	valueRange: [40, 70],
	axes: {
		y2: {
			// set axis-related properties here
			labelsKMB: true,
		},
	},
	ylabel: "Primary y-axis",
	y2label: "Secondary y-axis",
});

g2 = new Dygraph(document.getElementById("demodiv_one"), data, {
	labels: ["Date", "Y1", "Y2", "Y3", "Y4"],
	series: {
		Y3: { axis: "y2" },
		Y4: { axis: "y2" },
	},
	axes: {
		y: {
			valueRange: [40, 80],
		},
		y2: {
			// set axis-related properties here
			labelsKMB: true,
		},
	},
	ylabel: "Primary y-axis",
	y2label: "Secondary y-axis",
	axes: {
		y: {
			axisLabelWidth: 60,
		},
	},
});

g3 = new Dygraph(document.getElementById("demodiv_two"), data, {
	labels: ["Date", "Y1", "Y2", "Y3", "Y4"],
	series: {
		Y3: { axis: "y2" },
		Y4: { axis: "y2" },
	},
	axes: {
		y: {
			valueRange: [40, 80],
			axisLabelWidth: 60,
		},
		y2: {
			// set axis-related properties here
			valueRange: [1e6, 1.2e6],
			labelsKMB: true,
		},
	},
	ylabel: "Primary y-axis",
	y2label: "Secondary y-axis",
});
