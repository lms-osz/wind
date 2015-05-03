$(document).ready(function() {
    $("#day1").datepicker();
    $("#day2").datepicker();
    $("#day").datepicker();
    $("#day1").datepicker("option", "dateFormat", "dd.mm.yy");
    $("#day2").datepicker("option", "dateFormat", "dd.mm.yy");
    $("#day").datepicker("option", "dateFormat", "dd.mm.yy");
    
    var ctx = $("#Chart").get(0).getContext("2d");
    var myLineChart = new Chart(ctx).Line(data);
});
function convertToTimestamp(date, seperator) {
    date = date.split("seperator");
    var newDate = date[1] + "/" + date[0] + "/" + date[2];
    return new Date(newDate).getTime();
}
function onChangeDayToDay() {
    
}
function onChangeDayTime() {
    var day = $("#day").value;
    var hour = $("#hour").value;
    if (day.length < 0) {
        return 0;
    }
    json = '{"mode":"getData", "arg":[{"mode":"hour", "day":' + convertToTimestamp(day, ".") + ',"hour":' + hour + '}]}';
    
}
var data = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
        {
            label: "Wind Daten",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: [28, 48, 40, 19, 86, 27, 90]
        }
    ]
};
