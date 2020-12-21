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

var apartments = L.geoJSON(null, {
    style:function(feature) {

    },
    pointToLayer:function(feature, latlng) {

    }
});

apartments.addTo(map);

// fetch data from the db
// 
function fetchApartments(url) {
    fetch(url, {responseType:'text'})
    .then(res => res.text())
    .then(response => {
        console.log(response);

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
    
    console.log(paginators);
    paginators.forEach(paginator => {
        $(paginator).on("click", function(e) {
            e.preventDefault();

            let url = "/apartments-list" + paginator.getAttribute("href");
            console.log(url);
            
            getListing( url);
        });
    })
}