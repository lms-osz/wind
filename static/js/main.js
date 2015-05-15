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
		$('#wind-power').html(calc_wind(parsedJSON["data"][0]["wind"]));
                $("#change_receive_winddata-btn").css("display","block");
		if ($('#realtime_data') != null) {
			$('#rtd-wind').html(calc_wind(parsedJSON["data"][0]["wind"]))
			$('#rtd-Ubatt').html(calc_Ubatt(parsedJSON["data"][0]["Ubatt"]))
			$('#rtd-Ibatt').html(calc_Ibatt(parsedJSON["data"][0]["Ibatt"]))
		}
		
	} else if (parsedJSON.mode == "return_data") {
            
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
function calc_wind(data) {
    data = Math.round(((data * 0.00322 / 165 * 1000 - 4) * 50 / 16) * 100) / 100;
    return data;
}
function calc_Ubatt(data) {
    return Math.round(data * 0.01517 * 10) / 10;
}
function calc_Ibatt(data) {
    return Math.round(data * 0.0239 * 10) / 10;
}
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







///////////////////////////////////////////////////////////////
//                                                           //
//                     Connectig...                          //
//                                                           //
///////////////////////////////////////////////////////////////

ConnectWs();
