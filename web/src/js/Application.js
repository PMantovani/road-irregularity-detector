var app = angular.module("MyApp", ['ngAnimate', 'ngAria', 'ngMessages', 'ngMaterial']);

app.service('Map', function() {

    this.markers = [];
    this.heatLocations = [];

    this.init = function() {
        this.map = new google.maps.Map(
            document.getElementById("map")
        );

        this.heatmap = new google.maps.visualization.HeatmapLayer({
            data: this.heatLocations,
            dissipating: true,
            map: this.map
        });
    };

    this.addMarker = function(coordinates) {
        // Add marker to map
        var marker = new google.maps.Marker({
            map: this.map,
            position: coordinates,
            animation: google.maps.Animation.DROP
        });
        this.markers.push(marker);

        // Adjust map zoom to cover all markers
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0; i < this.markers.length; i++) {
            bounds.extend(this.markers[i].getPosition());
        }
        this.map.fitBounds(bounds);
    };

    this.clearMarkers = function() {
        for (var i=0; i<this.markers.length; i++) {
            this.markers[i].setMap(null);
        }
        this.markers = [];
        this.markers.length = 0;
    };

    this.replaceMarker = function(coordinates) {
        if (this.marker !== undefined) {
            this.marker.setMap(null);
        }
        this.marker = new google.maps.Marker({
            map: this.map,
            position: coordinates,
            animation: google.maps.Animation.DROP
        });
    };

    this.addHeatLocation = function(coordinates) {
        var latLng = new google.maps.LatLng(coordinates.lat, coordinates.lng);
        this.heatLocations.push(latLng);

        this.heatmap.setData(this.heatLocations);

        // Adjust map zoom to cover all markers
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0; i < this.heatLocations.length; i++) {
            bounds.extend(this.heatLocations[i]);
        }
        this.map.fitBounds(bounds);
    };

});

app.config(function($mdThemingProvider) {
    $mdThemingProvider.theme('default')
        .primaryPalette('red', {
            'default': '900'
        })
        .accentPalette('orange');
});

app.filter('formatDate', function() {
    return function(input) {
        if (typeof input === "string") {
            if (input.length > 10) {
                var year = input.substr(2,2);
                var month = input.substr(5,2);
                var day = input.substr(8,2);
                var time = input.substr(11,8);
                var monthStr = ["Jan", "Feb", "Mar", "Abr", "Mai", "Jun",
                                "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
                month = monthStr[month-1];
                input = time + " " + day + " " + month + " " + year;
            }
        }
        return input;
    }
});