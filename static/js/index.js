$(document).ready(function() {
    $("#day1").datepicker();
    $("#day2").datepicker();
    $("#day").datepicker();
    $("#day1").datepicker("option", "dateFormat", "dd.mm.yy");
    $("#day2").datepicker("option", "dateFormat", "dd.mm.yy");
    $("#day").datepicker("option", "dateFormat", "dd.mm.yy");
});
function convertToTimestamp(date, seperator) {
    date = date.split(seperator);
    var newDate = date[1] + "/" + date[0] + "/" + date[2];
    return new Date(newDate).getTime() / 1000;
}
function sendChartRequest() {
    var dayFrom = $("#day1").val();
    var dayTo = $("#day2").val();
    if (dayFrom.length < 1 || dayTo.length < 1) {
        return 0;
    }
    
    try {
        json = '{"mode":"getData", "arg":[{"mode":"day2day", "dateFrom":' + convertToTimestamp(dayFrom, ".") + ',"dateTo":' + convertToTimestamp(dayTo, ".") + '}]}';
        doSend(json);
    } catch (e) {
        // make an http-request to /api/getData with the argumets as GET parameters (?from=234234234&to=324234234)
    }
}
function showChart(json_array) {
    var chartLabels = [],chartSeries = [];
    var d;
    var error = false;
    for (var i = 0; i < json_array.steps; i = i + 1) {
        if (!(json_array["data"]["wind"][i] > 0)) {
            error = true;
            break;
        }
        chartSeries[i] = calc_wind(json_array["data"]["wind"][i])
    }
    if (error) {
        alert("Error: There are some unset data... Try another period...");
        return;
    }
    for (var i = 0; i < json_array.steps; i = i + 1) {
        d = new Date((json_array["from"] + (i * ((json_array["to"] - json_array["from"]) / json_array["steps"]))) * 1000);
        if (json_array["to"] - json_array["from"] == 86400) {
            chartLabels[i] = (d.getHours() + "");
        } else {
            chartLabels[i] = (d.getDate());
        }
    }
    new Chartist.Line('.ct-chart', {
  labels: chartLabels,
  series: [
    chartSeries
  ]
}, {
  fullWidth: true,
  chartPadding: {
    right: 40
  }
});

}
