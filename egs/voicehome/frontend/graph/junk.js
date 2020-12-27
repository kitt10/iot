g = new Dygraph(document.getElementById("div_g"), NoisyData, {
	errorBars: true,
	zoomCallback: function (minDate, maxDate, yRange) {
		showDimensions(minDate, maxDate, yRange);
	},
	drawCallback: function () {
		document.getElementById("zoomed").innerHTML = "" + this.isZoomed();
		document.getElementById("zoomedX").innerHTML = "" + this.isZoomed("x");
		document.getElementById("zoomedY").innerHTML = "" + this.isZoomed("y");
	},
});

// TODO(konigsberg): Implement a visualization that verifies that initial
// displays also show correctly.

// Pull an initial value for logging.
var minDate = g.xAxisRange()[0];
var maxDate = g.xAxisRange()[1];
var minValue = g.yAxisRange()[0];
var maxValue = g.yAxisRange()[1];
showDimensions(minDate, maxDate, [minValue, maxValue]);

function showDimensions(minDate, maxDate, yRanges) {
	showXDimensions(minDate, maxDate);
	showYDimensions(yRanges);
}

function showXDimensions(first, second) {
	var elem = document.getElementById("xdimensions");
	elem.innerHTML = "dateWindow : [" + first + ", " + second + "]";
}

function showYDimensions(ranges) {
	var elem = document.getElementById("ydimensions");
	elem.innerHTML = "valueRange : [" + ranges + "]";
}

function zoomGraphX(minDate, maxDate) {
	g.updateOptions({
		dateWindow: [minDate, maxDate],
	});
	showXDimensions(minDate, maxDate);
}

function zoomGraphY(minValue, maxValue) {
	g.updateOptions({
		valueRange: [minValue, maxValue],
	});
	showYDimensions(g.yAxisRanges());
}

function unzoomGraph() {
	g.updateOptions({
		dateWindow: null,
		valueRange: null,
	});
}

function panEdgeFraction(value) {
	g.updateOptions({ panEdgeFraction: value });
}
