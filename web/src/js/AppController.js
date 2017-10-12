app.controller("AppController", ["$scope", "$http", "Map", function($scope, $http, Map) {
    var self = this;
    self.detections = [];

    Map.init();

    this.findInMap = function(lat, lng) {
        var coordinates = {
            lat: parseFloat(lat),
            lng: parseFloat(lng)
        };
        Map.replaceMarker(coordinates);
    };

    $http.get("http://localhost:8080/api.php")
        .then(function success(response) {
            self.detections = response.data;
            for (var i=0; i<self.detections.length; i++) {
                var coordinates = { lat: parseFloat(self.detections[i].latitude),
                                    lng: parseFloat(self.detections[i].longitude)};
                //Map.addMarker(coordinates);
                Map.addHeatLocation(coordinates);
            }
        }, function error(response) {
           console.log("Error while fetching the data");
        });
}]);