var app = angular.module("MyApp", []);

app.service('Map', function($q) {

    this.init = function() {
        var options = {
            center: new google.maps.LatLng(40.7127837, -74.00594130000002),
            zoom: 13,
            disableDefaultUI: true
        };
        this.map = new google.maps.Map(
            document.getElementById("map"), options
        );
    };

    this.addMarker = function(coordinates) {
        this.marker = new google.maps.Marker({
            map: this.map,
            position: coordinates,
            animation: google.maps.Animation.DROP
        });
        this.map.setCenter(coordinates);
    };

});

app.controller("AppController", ["$scope", "$http", "Map", function($scope, $http, Map) {
    var self = this;
    self.detections = [];

    Map.init();

    $http.get("http://localhost:8080/api.php")
        .then(function success(response) {
            self.detections = response.data;
            for (var i=0; i<self.detections.length; i++) {
                var coordinates = { lat: parseFloat(self.detections[i].latitude),
                                    lng: parseFloat(self.detections[i].longitude)};
                Map.addMarker(coordinates);
            }
        }, function error(response) {
           console.log("Error while fetching the data");
        });
}]);