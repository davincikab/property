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

var userLocationMarker = L.marker([0,0]);

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
        let index = feature.properties.pk;

        let popupString = "<div class='popup-content'><img src='https://unsplash.it/id/"+index+"/200/75' class='img-top'>"+
        "<div class='d-flex'>"+
        "<span>2 <i class='fa fa-bath'></i></span>"+
        "<span>3 <i class='fa fa-bed'></i></span>"+
        "<span>130 <i class='fa fa-area-chart'></i></span>"+
        "</div>"+
        "<p class='my-1 px-2'> Ksh "+ feature.properties.price +"</p>"+
        "<p class='my-1 px-2'>"+ feature.properties.location +"</p>"+
        "<button class=' my-2 mx-2 px-2 btn btn-outline-primary btn-sm btn-direction' data-pk='" + feature.properties.pk +"'> Get Directions</button>";

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
    // createCard(properties.features.slice(0, 20));
    addDirectionListener();
})
.catch(error => {
    console.error(error);
});

// map events
map.on("popupopen", function(e) {
    addDirectionListener();
});

function addDirectionListener() {
    let directionBtns = document.querySelectorAll(".btn-direction");
    console.log(directionBtns);

    directionBtns.forEach(btn => {
        btn.addEventListener("click", function(e) {
            console.log(this);

            let propertyPk = btn.getAttribute("data-pk");
            let feature = properties.features.find(feature => feature.properties.pk == parseInt(propertyPk))
            let coordinates = feature.geometry.coordinates;
            updateDestination(coordinates);
        });
    });
}

// get listing
getListing("/filter-property?page=1");

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
                "<span>"+ feature.properties.square_feet +" <i class='fa fa-area-chart'></i></span>"+
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

$('#look-for').on("click", function(e) {
    let value = $("#query").val();
    let url = "/filter-property?page=1&query=" + value;
    getListing(url);
})

function getListing(url) {
    fetch(url,  { responseType:'text'})
    .then(res =>res.text())
    .then(data => {
        // console.log(data);
        cardList.innerHTML = data;

        updateCount();
        getPaginator();
    })
    .catch(error => {
        console.error(error);
    });
}

// paginator
function getPaginator() {
    let paginators = document.querySelectorAll(".paginator");
    
    console.log(paginators);
    paginators.forEach(paginator => {
        $(paginator).on("click", function(e) {
            e.preventDefault();

            let url = "/filter-property" + paginator.getAttribute("href");
            console.log(url);
            
            getListing( url);
        });
    })
}

function updateCount() {
    console.log("Updating count");
    
    let count = $(".card-item").length;
    let text = count + " houses found";

    $('#property-count').text(text);
}

// toggle list and box mode
let displayModes = document.querySelectorAll(".display-mode");
displayModes.forEach(displayMode => {
    $(displayMode).on('click', function(e) {
        displayModes.forEach(displayMode =>  displayMode.classList.remove("active"));

        if(displayMode.classList.contains("fa-list")) {
            cardList.classList.remove("table-view");
            displayMode.classList.add("active");
            return;
        }

        displayMode.classList.add("active");
        cardList.classList.add("table-view");
    });
});

 
function updateDestination(coordinates) {
    // update the destination
    let latLng = L.latLng(coordinates.reverse());
    let waypoints = routerControl.getWaypoints();

    routerControl.setWaypoints([
        waypoints[0].latLng,
        latLng
    ]);
}

// geolocation control
var geolocationControl = new L.Control({position:"topleft"});
geolocationControl.onAdd = function(map) {
    let div = L.DomUtil.create("button", "btn btn-locate");

    div.innerHTML = "<img src='/static/images/geolocate.svg' alt='geolocate'>";

    div.addEventListener("click", function(e) {
        map.locate();
    });

    return div;
}

map.addControl(geolocationControl);

// map location event
map.on("locationfound", function(e) {
    // get the user location
    console.log(e);

    // flyto user location
    map.flyTo(e.latlng, 16);

    // add user location marker
    userLocationMarker.setLatLng(e.latlng).addTo(map);

    // update waypoints
    let waypoints = routerControl.getWaypoints();

    routerControl.setWaypoints([
        e.latlng,
        waypoints[1].latLng,
    ]);
    
});

map.on("locationerror", function(e) {
    console.log(e);
});

// create a routing control
var routerControl = L.Routing.control({
    router: L.Routing.mapbox('pk.eyJ1IjoiZGF1ZGk5NyIsImEiOiJjanJtY3B1bjYwZ3F2NGFvOXZ1a29iMmp6In0.9ZdvuGInodgDk7cv-KlujA'),
    collapsible:true,
    waypoints: [],
    geocoder: L.Control.Geocoder.nominatim(),
    createMarker: function(i, wp) {
          var options = {
        },
          
        marker = L.marker(wp.latLng, options);
        return false;
    },
    lineOptions:{
        styles:[
            {color: '#666', opacity: 1, weight: 2}
        ],
        addWaypoints:false
    }
}).addTo(map);

routerControl.on("routesfound", function(e) {
    console.log(e);
});

// TODO: Toggle filter section: bed, bathroom, price, 
// Marker cluster
// Active element and scroll to
// spinner