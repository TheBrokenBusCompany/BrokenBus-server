// initialize the map
var map = L.map('map').setView([36.711, -4.422], 13);

// load a tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
        attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
        maxZoom: 19,
        minZoom: 2
    }).addTo(map);

// Create geoJSON layer and start refresh cycle
var geoJSONLayer = L.geoJSON().addTo(map);
setUpLayer(geoJSONLayer);
refresh();