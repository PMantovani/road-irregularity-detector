class MapService {
    constructor() {
        this.markers = [];
        this.detectionsPolylines = [];
    }

    init() {
        this.map = new google.maps.Map(
            document.getElementById("map"),
            { zoom: 16,
            center: {lat: -25.451290, lng: -49.233795} }
        );
    };

    getMapBounds() {
        return this.map.getBounds().toJSON();
    }

    addMarker(coordinates) {
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

    clearMarkers() {
        for (var i=0; i<this.markers.length; i++) {
            this.markers[i].setMap(null);
        }
        this.markers = [];
        this.markers.length = 0;
    };

    replaceMarker(coordinates) {
        if (this.marker !== undefined) {
            this.marker.setMap(null);
        }
        this.marker = new google.maps.Marker({
            map: this.map,
            position: coordinates,
            animation: google.maps.Animation.DROP
        });
        var latLng = new google.maps.LatLng(coordinates.lat, coordinates.lng);
        this.map.setCenter(latLng);
    };

    clearDetections() {
        for (var i=0; i<this.detectionsPolylines.length; i++) {
            this.detectionsPolylines[i].setMap(null);
        }
        this.detectionsPolylines = [];
    };

    addDetection(detection) {
        var quality = detection.quality;
        var path = detection.path;

        if (parseInt(quality) === 1) {
            var lineColor = '#FF0000';
        } else if (parseInt(quality) === 2) {
            lineColor = '#FFFF00';
        } else if (parseInt(quality) === 3) {
            lineColor = '#00FF00';
        }

        var polyline = new google.maps.Polyline({
            path: path,
            strokeColor: lineColor,
            strokeOpacity: 0.50,
            strokeWeight: 5
        });

        this.attachInfoWindow(polyline, detection);

        polyline.setMap(this.map);
        this.detectionsPolylines.push(polyline);
    }

    attachInfoWindow(element, detectionInfo) {
        if (detectionInfo.quality < 3) {
            var quality = 'Bad';
        }
        else {
            quality = 'Good';
        }
        var reading_date = new Date(detectionInfo.reading_date);
        var contentHtml = 'Road Quality:      ' + quality + '</br>' +
                          'Sensor Id:         ' + detectionInfo.sensor_id + '</br>' +
                          'Mean Speed:        ' + detectionInfo.speed + ' km/h</br>' +
                          'Date of Detection: ' + reading_date.toUTCString();

        var infoWindow = new google.maps.InfoWindow({
            content: contentHtml
        });

        element.addListener('click', function(e) {
            var clickLatLng = e.latLng;
            infoWindow.setPosition(clickLatLng);
            infoWindow.open(element.get('map'));    
        });
    }

    addEventOnBoundChanged(callback) {
        google.maps.event.addListener(this.map, "idle", callback);
    }
}