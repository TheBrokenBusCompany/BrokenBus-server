var geoJSONLayer = null;
var user = null;
const busesEndpoint = 'http://localhost:5000/api/v1/buses/geojson';
const stopsEndpoint = 'http://localhost:5000/api/v1/stops/geojson';

function onSignIn(googleUser) {
    /*
     * Called only by the google sign in button
     * Logs the user in and hides itself while showing the user
     */
    user = googleUser.getBasicProfile();
    console.log('ID: ' + user.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + user.getName());
    console.log('Image URL: ' + user.getImageUrl());
    console.log('Email: ' + user.getEmail()); // This is null if the 'email' scope is not present.

    document.getElementById("userName").innerText = user.getName();
    document.getElementById("profilePicture").src = user.getImageUrl();

    document.getElementById('googleSignIn').style.display = 'none';
    document.getElementById('googleUser').style.display = 'inherit';
}

function onError(response) {
    /*
     * Called only by the google sign in button
     * in case of error.
     */
    console.log('Error on OAuth:' + response);
}

function signOut() {
    /*
     * Logs out the user, hides itself and shows
     * the google sign in button again.
     */
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });

    document.getElementById("userName").innerText = '';
    document.getElementById("profilePicture").src = '';
    document.getElementById('googleSignIn').style.display = 'inherit';
    document.getElementById('googleUser').style.display = 'none';
}

function sleep(ms) {
    /*
     * Async sleep function
     */
    return new Promise(resolve => setTimeout(resolve, ms));
}

function setUpLayer(layer) {
    /*
     * Prepare the geoJSON layer global variable for other uses
     */
    geoJSONLayer = layer;


}

function httpGetAsync(url, callback, errorCallback) {
    /*
     * Async HTTP get request
     * https://stackoverflow.com/a/4033310
     * xmlHttp.readyState 4 is DONE
     */
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.response);
        else if(xmlHttp.readyState == 4)
            errorCallback(xmlHttp.status);
    }
    xmlHttp.open("GET", url, true); // true for asynchronous 
    xmlHttp.send(null);
}

async function refresh() {
    /*
     * Refreshes the bus positions in the map
     * Runs in loop every minute to update the positions
     */
    httpGetAsync(busesEndpoint, function(response) {   
        console.log('Updating buses position');
        //geoJSONLayer.clearLayers();
        //geoJSONLayer.addData(JSON.parse(response));
        var myIcon = new L.icon({ 
            iconUrl: '/static/icon/icon_bus.png',
            iconSize: [27, 27],
            iconAnchor: [13, 27]
        }); 
        L.geoJSON(JSON.parse(response), {
            pointToLayer: function (feature, latlng) {
                return L.marker(latlng, {icon: myIcon});
            }
        }).addTo(map);
        // Remove error toast on success
        document.getElementById('updateErrorToast').className = '';
    }, function(response) {
        // Show error toast on error
        console.log('Error on update state = ' + response);
        document.getElementById('updateErrorToast').className = 'show';
    });


    await sleep(60000); // Sleep for a minute
    refresh();
}

async function showStops() {
    /*
     * Refreshes the bus positions in the map
     * Runs in loop every minute to update the positions
     */
    httpGetAsync(stopsEndpoint, function(response) {   
        console.log('Showing stops position');
        //geoJSONLayer.clearLayers();
        //geoJSONLayer.addData(JSON.parse(response));
        var myIcon = new L.icon({ 
            iconUrl: '/static/icon/icon_stop_black.png',
            iconSize: [27, 27],
            iconAnchor: [13, 27]
        });
        L.geoJSON(JSON.parse(response), {
            pointToLayer: function (feature, latlng) {
                return L.marker(latlng, myIcon);
            }
        }).addTo(map);
        // Remove error toast on success
        document.getElementById('updateErrorToast').className = '';
    }, function(response) {
        // Show error toast on error
        console.log('Error on update state = ' + response);
        document.getElementById('updateErrorToast').className = 'show';
        showStops();
    });
}