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
		onOpen(evt)
	};
	websocket.onclose = function(evt) {
		onClose(evt)
	};
	websocket.onmessage = function(evt) {
		onMessage(evt)
	};
	websocket.onerror = function(evt) {
		onError(evt)
	};
}
$(document).ready(function() {
	ConnectWs();
});

function onOpen(evt) {
	console.log("opened")
	$("#disconnected-ws").css("display", "none");
}

function onClose(evt) {
	console.log("DISCONNECTED");
	$("#disconnected-ws").css("display", "block");
	setTimeout(function() {
		ConnectWs()
	}, 2000);
}

function onMessage(evt) {
	console.log(evt.data);
	$('#wind').val(evt.data);
}

function onError(evt) {
	console.log(evt.data);
}

function doSend(message) {
	console.log("SENT: " + message);
	websocket.send(message);
}
