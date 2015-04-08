// websocket stuff
if (window.location.protocol == "http:") {
    wsprotocol = "ws://";
} else {
    wsprotocol = "wss://";
}
websocketurl = wsprotocol + location.hostname+(location.port ? ':'+location.port: '') + "/ws";

function ConnectWs() {
	try {
		websocket = new WebSocket(websocketurl);
	} catch (e) {
		return;
	}
	websocket.onopen = function(evt) {
		onOpen(evt);
	};
	websocket.onclose = function(evt) {
		onClose(evt);
	};
	websocket.onmessage = function(evt) {
		onMessage(evt);
	};
	websocket.onerror = function(evt) {
		onError(evt);
	};
}
/***********************************************
 *       connecting to the websocket           *
 ***********************************************/
$(document).ready(function() {
	ConnectWs();
});

function onOpen(evt) {
	console.log("opened")
	$("#disconnected-ws").css("display", "none");
        doSend('{"client":"web","realtimedata":' + receive_winddata + '}');
}

function onClose(evt) {
	console.log("DISCONNECTED");
	$("#disconnected-ws").css("display", "block");
	setTimeout(function() {
		ConnectWs();
	}, 2000);
}

function onMessage(evt) {
	console.log("RECEIVE: " + evt.data);
        var parsedJSON = jQuery.parseJSON(evt.data);
        if (parsedJSON.mode == "update") {
		$('#wind-power').html(parsedJSON.data);
                $("#change_receive_winddata-btn").css("display","block");
	}
}

function onError(evt) {
	console.log(evt.data);
}

function doSend(message) {
	console.log("SENT: " + message);
	websocket.send(message);
}
/***********************************************
 *                   Chart                     *
 ***********************************************/
$(document).ready(function() {
    var ctx = $("#Chart").get(0).getContext("2d");
    var myLineChart = new Chart(ctx).Line(data);
});
var data = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
        {
            label: "Wind Data",
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
// other stuff
function about_window(open) {
    var panal = "#about_panal";
    var blackout = "#blackout";
    if (open) {
        $(panal).css("display","block");
        $(blackout).css("display","block");
    } else {
        $(panal).css("display","none");
        $(blackout).css("display","none");
    }
}
receive_winddata = true;
function change_receive_winddata() {
    if (receive_winddata == true) {
        $("#not_receive_winddata").css("display","none");
        $("#receive_winddata").css("display","block");
    } else {
        $("#not_receive_winddata").css("display","block");
        $("#receive_winddata").css("display","none");
    }
    receive_winddata = !receive_winddata;
    doSend('{"realtimedata":' + receive_winddata + '}');
}
document.onkeydown = function(event) {
    if (event.keyCode == 27) {
        about_window(false)
    }
}