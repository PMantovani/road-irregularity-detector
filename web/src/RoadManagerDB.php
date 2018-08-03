<?php

require_once('MissingFieldsException.php');
require_once('DbOperationException.php');
require_once('RoadsGoogleApi.php');
require_once('RoadsGoogleApiException.php');

class RoadManagerDB {

    public function __construct() {
        $this->db = new mysqli("localhost", "root", "root12mysql!", "roadmanager");
    }

    public function getDetections(array $filters) {

        $num_params = "";
        $query = "SELECT detections.id, detections.sensor_id, detections.speed, detections.course,
                         detections.quality, detections.reading_date, 
                         detections_path.latitude, detections_path.longitude FROM detections
                         INNER JOIN detections_path ON detections.id = detections_path.detection_id";
        $params = [];

        if (sizeof($filters) > 0) {
            $query .= ' WHERE ';
        }

        foreach($filters as $key => $value) {
            switch ($key) {
                case 'south':
                    $query .= 'AND start_latitude >= ? ';
                    break;
                case 'north':
                    $query .= 'AND start_latitude <= ? ';
                    break;
                case 'west':
                    $query .= 'AND start_longitude >= ? ';
                    break;
                case 'east':
                    $query .= 'AND start_longitude <= ? ';
                    break;
                case 'onlyBadRoads':
                    $query .= 'AND quality < ? ';
                    $value = '3';
                    break;
                case 'fromDate':
                    $query .= 'AND reading_date >= ? ';
                    break;
                default:
                    $query .= " AND " . $key . "= ? ";
                break;
            }
            $params[] = $value;
            $num_params .= "s";
        }
        $query .= 'LIMIT 5000;';

        // Remove aditional AND right after the WHERE clause
        $query = str_replace('WHERE AND', 'WHERE', $query);
            
        $stmt = $this->db->prepare($query);
        $stmt->bind_param($num_params, ...$params);

        $stmt->execute();

        if($result = $stmt->get_result()) {
            return $this->formatDetections($result->fetch_all(MYSQLI_ASSOC));
        }
    }

    public function insertDetection(array $data) {
        $key_params = ['sensor_id', 'start_latitude', 'start_longitude', 'end_latitude',
                       'end_longitude', 'speed', 'course', 'quality', 'reading_date'];

        for ($i=0; $i<sizeof($key_params); $i++) {
            if (!array_key_exists($key_params[$i], $data)) {
                throw new MissingFieldsException();
            }
        }

        $query = 'INSERT INTO detections 
                    (sensor_id, start_latitude, start_longitude, end_latitude, 
                     end_longitude, speed, course, quality, reading_date, created_date) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NOW());';

        if ($stmt = $this->db->prepare($query)) {
            $stmt->bind_param("sssssssss", ...array_values($data));
            if(!$stmt->execute()) {
                throw new DbOperationException();
            }
            return $this->db->insert_id;
        }
    }

    public function insertDetectionPath(int $detection_id, float $start_lat, float $start_lng, float $end_lat, float $end_lng) {
        $roadsApi = new RoadsGoogleApi();

        $snappedPoints = $roadsApi->snapToRoads($start_lat, $start_lng, $end_lat, $end_lng);

        if (array_key_exists('error', $snappedPoints)) {
            throw new RoadsGoogleApiException($snappedPoints['error']['message']);
        }

        $snappedPoints = $snappedPoints['snappedPoints'];
        $query = 'INSERT INTO detections_path (detection_id, path_counter, latitude, longitude) VALUES (?, ?, ?, ?);';
        
        if ($stmt = $this->db->prepare($query)) {

            for ($i=0; $i<count($snappedPoints); $i++) {
                $coordinates = $snappedPoints[$i]['location'];
                $path_count = $i + 1;
                $stmt->bind_param("ssss", $detection_id, $path_count, $coordinates['latitude'], $coordinates['longitude']);

                if(!$stmt->execute()) {
                    throw new DbOperationException();
                }
            }
        }

        $stmt->close();
        return true;
    }

    private function formatDetections(array $detections): array {
        $formatted = [];

        for($i=0; $i<count($detections); $i++) {
            if ($i == 0) {
                $previousId = $detections[$i]['id'];
                $path = [];
            }
            else if ($previousId !== $detections[$i]['id']) {
                $detection = [];
                $detection['id']           = $detections[$i-1]['id'];
                $detection['sensor_id']    = $detections[$i-1]['sensor_id'];
                $detection['speed']        = $detections[$i-1]['speed'];
                $detection['course']       = $detections[$i-1]['course'];
                $detection['quality']      = $detections[$i-1]['quality'];
                $detection['reading_date'] = $detections[$i-1]['reading_date'];
                $detection['path'] = $path;
                $formatted[] = $detection;
                $path = [];
                $previousId = $detections[$i]['id'];
            }

            $latLngPair = [];
            $latLngPair['lat'] = $detections[$i]['latitude'];
            $latLngPair['lng'] = $detections[$i]['longitude'];
            $path[] = $latLngPair;
        }
        if ($i > 0) {
            $i--;
            $detection = [];
            $detection['id']           = $detections[$i]['id'];
            $detection['sensor_id']    = $detections[$i]['sensor_id'];
            $detection['speed']        = $detections[$i]['speed'];
            $detection['course']       = $detections[$i]['course'];
            $detection['quality']      = $detections[$i]['quality'];
            $detection['reading_date'] = $detections[$i]['reading_date'];
            $detection['path'] = $path;
            $formatted[] = $detection;
        }

        return $formatted;
    }
}