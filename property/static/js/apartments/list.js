var map = L.map('map',{
    zoom:12,
    center:{lat: -1.4041005485564289, lng: 36.72112131585477}
});

var accessToken = 'pk.eyJ1IjoiZGF1ZGk5NyIsImEiOiJjanJtY3B1bjYwZ3F2NGFvOXZ1a29iMmp6In0.9ZdvuGInodgDk7cv-KlujA';

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token='+ accessToken , {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: accessToken
}).addTo(map);

let propertyIcon =  L.icon({
    iconUrl:"/static/images/home.png",
    iconSize:[28, 28]
});

var apartments = L.geoJSON(null, {
    style:function(feature) {

    },
    onEachFeature:function(feature, layer) {
        let popupString = "<div class='popup-content'><h5 class='title'>"+ feature.properties.name +"</h5>" +
        "<p class='my-1 px-2'> <b>Location </b> "+ feature.properties.location +"</p>"+
        "<b class='my-1 px-2'>House Types</b>"+
        "<p class='my-1 px-2'>"+ feature.properties.house_types +"</p>"+
        "</div>";

        layer.bindPopup(popupString);
    },
    pointToLayer:function(feature, latlng) {
        return L.marker(latlng, {icon:propertyIcon});
    }
});

apartments.addTo(map);

// get apartments
fetch("/apartments-data/")
.then(res => res.json())
.then(data => {
    console.log(data);
    apartments.addData(data);
    
    if(apartments.getBounds()._northEast) {
        map.fitBounds(apartments.getBounds());
    }
})
.catch(error => {
    console.error(error);
});

// fetch data from the db
// 
function fetchApartments(url) {
    fetch(url, {responseType:'text'})
    .then(res => res.text())
    .then(response => {

        $("#aparment-list").html(response);
        getPaginator();

    })
    .catch(error => {
        console.log(error);
    });
}

fetchApartments('/apartments-list/?page=1');

// clicking or previous button
// paginator
function getPaginator() {
    let paginators = document.querySelectorAll(".paginator");

    paginators.forEach(paginator => {
        $(paginator).on("click", function(e) {
            e.preventDefault();

            let url = "/apartments-list" + paginator.getAttribute("href");
            console.log(url);
            
            fetchApartments( url);
        });
    })
}


// filter
var searchForm = $("#search-form");
var searchField = $("#search");

searchForm.on("submit", function(e) {
    e.preventDefault();

    // get the form value
    let value = searchField.val();

    let url = "/apartments-list/?page=1&query=" + value;
    if(value == "") {
        url = "/apartments-list/?page=1";
    }

    // fetch the data
    console.log(url);
            
    fetchApartments(url);
});