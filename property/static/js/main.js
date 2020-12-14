var lat = 0.9887;
var lng = 37.998;
var properties;

var accessToken = 'pk.eyJ1IjoiZGF1ZGk5NyIsImEiOiJjanJtY3B1bjYwZ3F2NGFvOXZ1a29iMmp6In0.9ZdvuGInodgDk7cv-KlujA';
var cardList = document.getElementById("card-list");
var containerElement = document.getElementById('container');
var mapToggler = document.getElementById('map-toggler');
var filterToggler = document.getElementById("collapse-filter");
var filterSection = document.getElementById("filter-section");

var map = L.map('mapContainer',{
    zoom:12,
    center:{lat: -1.4041005485564289, lng: 36.72112131585477}
});

var propertyIcon = L.divIcon({
    className:'property-marker',
    html:""
});

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token='+ accessToken , {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: accessToken
}).addTo(map);


var property = L.geoJSON(null, {
    onEachFeature:function(feature, layer) {
        let index = feature.properties.objectid;

        let popupString = "<div class='popup-content'><img src='https://unsplash.it/id/"+index+"/200/75' class='img-top'>"+
        "<div class='d-flex'>"+
        "<span>2 <i class='fa fa-bath'></i></span>"+
        "<span>3 <i class='fa fa-bed'></i></span>"+
        "<span>130 <i class='fa fa-area-chart'></i></span>"+
        "</div>";

        layer.bindPopup(popupString);
    },
    pointToLayer:function(feature, latLng) {
        return L.marker(latLng,{icon:propertyIcon});
    }
}).addTo(map);
// var propertyMarker = L.marker([lat, lng], {icon:propertyIcon})
//     .bindPopup(popuString);


fetch('/property-data/')
.then(response => response.json())
.then(data => {
    properties = data;
    property.addData(data);

    // display the first 20 
    createCard(properties.features.slice(0, 20));
})
.catch(error => {
    console.error(error);
});

function createCard(data) {
    let cardListString = "";

    data.forEach((feature) => {
        let index = feature.properties.pk;
        cardListString += '<figure class="card-item">'+
        '<img src="https://unsplash.it/id/'+ index +'/300/200" class="img" alt="Place name">'+
        '<figcaption class="ml-3">'+
            "<h2><a href='/detail/" + feature.properties.slug +"' class='title'>" + feature.properties.title + "</a></h2>"+
            '<div class="details-section">'+
                '<span>' + feature.properties.location+'</span>'+
                '<span class="bold"> Ksh. ' + feature.properties.price +'</span>'+
            '</div>'+
            "<div class='d-flex px-0'>"+
                "<span>"+ feature.properties.baths +" <i class='fa fa-bath'></i></span>"+
                "<span>"+ feature.properties.beds +" <i class='fa fa-bed'></i></span>"+
                "<span>13"+ feature.properties.square_feet +" <i class='fa fa-area-chart'></i></span>"+
            "</div>"+
       ' </figcaption>'+
        '</figure>'
    });

    cardList.innerHTML = cardListString;
}

// toggle map
mapToggler.addEventListener('click', function(e) {
    if(e.target.checked) {
        containerElement.classList.add('close-map');
    } else {
        containerElement.classList.remove('close-map');
    }
});

filterToggler.addEventListener('click', function(e) {
    filterSection.classList.toggle("collapse-section");
});

// TODO: Toggle filter section: bed, bathroom, price, 
// Marker cluster
// Active element and scroll to
// pagination
// spinner
// Map toggler