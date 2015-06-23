$(document).ready(function() {
    $("#day1").datepicker();
    $("#day2").datepicker();
    $("#day").datepicker();
    $("#day1").datepicker("option", "dateFormat", "dd.mm.yy");
    $("#day2").datepicker("option", "dateFormat", "dd.mm.yy");
    $("#day").datepicker("option", "dateFormat", "dd.mm.yy");
});
function showLoading(show) {
    if (show) {
        $("#loading-blackout").show()
        $("#loading-text").show()
    } else {
        $("#loading-blackout").hide()
        $("#loading-text").hide()
    }
}
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
        showLoading(true);
    } catch (e) {
        // make an http-request to /api/getData with the argumets as GET parameters (?from=234234234&to=324234234)
    }
}
function showChart(json_array) {
    showLoading(false);
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
        if (showChartError) {
            alert("Error: There are some unset data... Try another period...");
        }
        return;
    }
    for (var i = 0; i < json_array.steps; i = i + 1) {
        d = new Date((json_array["from"] + (i * ((json_array["to"] - json_array["from"]) / json_array["steps"]))) * 1000);
        if (json_array["to"] - json_array["from"] == 86400) {
            chartLabels[i] = (d.getHours() + "");
        } else {
            chartLabels[i] = (d.getDate() + "." + (d.getMonth() + 1) + "<br>" +  d.getHours() + ":00");
        }
    }
    new Chartist.Line('.ct-chart', {
        labels: chartLabels,
        series: [
            {
                name: "Wind",
                data: chartSeries
            }
        ]
       }, {
          fullWidth: true,
          high: 10,
          low: 0,
          chartPadding: {
              right: 40
          },
          axisY: {
              onlyInteger: true,
              offset: 20
          },
    });
    var chart = $('.ct-chart');

var $toolTip = chart
  .append('<div class="tooltip"></div>')
  .find('.tooltip')
  .hide();

chart.on('mouseenter', '.ct-point', function() {
    var point = $(this),
    value = point.attr('ct:value'),
    seriesName = point.parent().attr('ct:series-name');
  $toolTip.html(seriesName + '<br>' + value + " m/s").show();
});

chart.on('mouseleave', '.ct-point', function() {
  $toolTip.hide();
});

chart.on('mousemove', function(event) {
  $toolTip.css({
    left: (event.offsetX || event.originalEvent.layerX) - $toolTip.width() / 2 - 10,
    top: (event.offsetY || event.originalEvent.layerY) - $toolTip.height() - 40
  });
});
showChartError = true;
}

showChartError = false;

function getChartOfToday() {
    var now = new Date();
    var dayTo = new Date(now.getFullYear(), now.getMonth(), now.getDate()) / 1000;
    var dayFrom = dayTo - 86400;
    json = '{"mode":"getData", "arg":[{"mode":"day2day", "dateFrom":' + dayFrom + ',"dateTo":' + dayTo + '}]}';
    doSend(json);
}
