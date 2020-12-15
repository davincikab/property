var accessToken = 'pk.eyJ1IjoiZGF1ZGk5NyIsImEiOiJjanJtY3B1bjYwZ3F2NGFvOXZ1a29iMmp6In0.9ZdvuGInodgDk7cv-KlujA';
var propertyLocation = $("#property-location");

let center = propertyLocation.text().trim();
center = center != "None" ? center.match(/(.[0-9])\.([0-9]){5,15}/g) : {lat: -1.4041005485564289, lng: 36.72112131585477};

console.log(center);
center = (center instanceof Array) ? center.map(ct => parseFloat(ct)).reverse() : center;

var map  = L.map('map', { 
    zoom:12,
    center:center
});

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token='+ accessToken , {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: accessToken
}).addTo(map);

var marker = L.marker(center, {
    draggable:true
}).addTo(map);

marker.on("dragend", function(e) {
    // update the coordinates
    let coord = e.target.getLatLng();
    let val = "SRID=4326;POINT ("+ coord.lng +" "+ coord.lat +")";
    $("#id_geom").val(val);

    // geocode the coordinates
    geocodeLocation(coord);
});

// map interaction
map.on("click", function(e) {

});

// get the location coordinates: mapbox place API
function geocodeLocation(coord) {
    let endpoint = "geocoding/v5/mapbox.places/"+ coord.lng +"," + coord.lat + ".json";
    let url = "https://api.mapbox.com/" + endpoint + "?access_token=" + accessToken;

    fetch(url)
    .then(res => res.json())
    .then(places => {
        console.log(places);
        if(places.features.length > 0) {
            let place_name = places.features[0].place_name;

            $('#id_location').val(place_name);
        }
    })
    .catch(error => {
        console.error(error);
    });
}