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
// other stuff
/*function about_window(open) {
    var panal = "#about_panal";
    var blackout = "#blackout";
    if (open) {
        $(panal).css("display","block");
        $(blackout).css("display","block");
    } else {
        $(panal).css("display","none");
        $(blackout).css("display","none");
    }
}*/
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

