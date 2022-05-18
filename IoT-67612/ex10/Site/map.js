import {generateMarker} from "./MarkerGenerator.js";

var client;
var reconnectTimeout = 2000;
var host = "broker.mqttdashboard.com";
var port = 8000;
var topic = "huji_iot_class/2021_2022/smarTrash";
var qos = "0";
var CenterPoint = [21.002902, 52.228850];
var map;
var markers;
var MAX_DISTANCE = 100.0;
var ID_TO_MSGS_MAP = new Map();
var ID_TO_MARKER_MAP = new Map();


function onConnect() {
    console.log("Connected ");
    client.subscribe(topic, {qos: Number(qos)});
}

function onMessageArrive(message) {
    console.log("onMessageArrived:" + message.payloadString);
    message = JSON.parse(message.payloadString);

    let cur_distance_percents =  100*Number(Math.min(100, message.distance)) / MAX_DISTANCE;
    let id = message.id;

    let lat = Math.floor(Number(message.lat)/(100*Number(message.lat_scale))) + (Number(message.lat)%(100*Number(message.lat_scale)))/(60*Number(message.lat_scale));
    let long = Math.floor(Number(message.long)/(100*Number(message.long_scale))) + (Number(message.long)%(100*Number(message.long_scale)))/(60*Number(message.lat_scale));

    let curMarkerImage = generateMarker(cur_distance_percents);
    let curMarker = addMapMarker(lat, long, curMarkerImage);

    if (ID_TO_MARKER_MAP.has(id)) {
        ID_TO_MSGS_MAP.get(id).push(message);
        ID_TO_MARKER_MAP.get(id).setMap(null);
        ID_TO_MARKER_MAP.set(id, curMarker);
    } else {
        ID_TO_MSGS_MAP.set(id, [message]);
        ID_TO_MARKER_MAP.set(id, curMarker);
    }
}

function addMapMarker(lat, lng, markerImage) {
    // The marker, positioned at Uluru
    const marker = new google.maps.Marker({
        position: new google.maps.LatLng(lat, lng),
        map: map,
        icon: markerImage,
        title:"Hello World!"
    });
    console.log(lat);
    marker.setMap(map);
    return marker;
}

function initMap() {
    // The location of HUJI
    const huji_loc = {lat: 31.77480304008521, lng: 35.19783738032892};
    // The map, centered at Uluru
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: huji_loc,
    });
}


function Init() {
    console.log("connecting to " + host + " " + port);
    client = new Paho.MQTT.Client(host, port, "clientjs");
    //document.write("connecting to "+ host);
    var options = {
        //useSSL:true,
        timeout: 3,
        onSuccess: onConnect
    };
    client.onMessageArrived = onMessageArrive;
    client.connect(options); //connect
    initMap()
}

window.onload = Init;
