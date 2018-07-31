app.controller("AppController", ["$scope", "$http", "Map", function($scope, $http, Map) {
    var self = this;
    self.detections = [];
    self.dateRange = "1";
    self.showOnlyBadRoads = false;

    Map.init();

    this.findInMap = function(lat, lng) {
        var coordinates = {
            lat: parseFloat(lat),
            lng: parseFloat(lng)
        };
        Map.replaceMarker(coordinates);
    };

    self.onBadRoadSwitchChange = function() {
        self.requestDetections();
    };

    self.calculateQueryDateTime = function(dateRange) {
        const secsInAMonth = (30*24*60*60*1000);
        var fromDate = new Date();
        fromDate.setTime(fromDate.getTime() - secsInAMonth * parseInt(dateRange));

        return fromDate.toISOString();
    }

    self.requestDetections = function() {
        var bounds = Map.getMapBounds();
        var url = "http://localhost/api.php?north=" + bounds.north +
                                           "&south=" + bounds.south + 
                                           "&west="  + bounds.west +
                                           "&east="  + bounds.east;
        if (self.showOnlyBadRoads) {
            url += "&onlyBadRoads=True";
        }
        url += "&fromDate=" + self.calculateQueryDateTime(self.dateRange);

        $http.get(url).then(function success(response) {
            self.detections = response.data;

            Map.clearDetections(self.dateRange);
            for (var i=0; i<self.detections.length; i++) {
                var start_coordinates = { lat: parseFloat(self.detections[i].start_latitude),
                                          lng: parseFloat(self.detections[i].start_longitude)};
                var end_coordinates = { lat: parseFloat(self.detections[i].end_latitude),
                                        lng: parseFloat(self.detections[i].end_longitude)};

                Map.addDetection(start_coordinates, end_coordinates, self.detections[i].quality);
            }
        }, function error(response) {
           console.log("Error while fetching the data");
        });
    };

    Map.addEventOnBoundChanged(self.requestDetections);

}]);
