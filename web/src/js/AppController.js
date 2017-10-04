var app = angular.module("MyApp", []);

app.controller("AppController", ["$scope", "$http", function($scope, $http) {
    var self = this;
    self.detections = [];

    $http.get("http://localhost:8080/api.php")
        .then(function success(response) {
            self.detections = response.data;
        }, function error(response) {
           console.log("Error while fetching the data");
        });
}]);