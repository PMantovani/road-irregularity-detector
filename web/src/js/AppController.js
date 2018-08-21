app.controller("AppController", ["$scope", "$http", "Map", function($scope, $http, Map) {
    var self = this;
    self.sensors = [];
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

    self.calculateQueryDateTime = function(numberOfWeeks) {
        const secsInAWeek = (7*24*60*60*1000);
        var fromDate = new Date();
        fromDate.setTime(fromDate.getTime() - secsInAWeek * parseInt(numberOfWeeks));

        return fromDate.toISOString();
    }

    self.requestDetections = function() {
        var bounds = Map.getMapBounds();
        var url = "http://localhost/api.php/detections?north=" + bounds.north +
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
                Map.addDetection(self.detections[i]);
            }
        }, function error(response) {
           console.log("Error while fetching the data");
        });
    };

    self.requestSensors = function() {
        var url = "http://localhost/api.php/sensors";

        $http.get(url).then(function success(response) {
            self.sensors = response.data;
        }, function error(response) {
            console.log("Error while fetching the data: " + response.data);
        });
    };

    self.onSensorClick = function(lat, lng) {
        Map.replaceMarker({lat: lat, lng: lng});
    }

    self.requestSensors();
    Map.addEventOnBoundChanged(self.requestDetections);

}]);
