<?php

class RoadManagerDB {

    public function __construct() {
        $this->db = new mysqli("localhost", "root", "root12mysql!", "roadmanager");
    }

    public function getDetections($filters) {

        $num_params = "";
        $query = "SELECT * FROM detections";
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
        $query .= 'LIMIT 500;';

        // Remove aditional AND right after the WHERE clause
        $query = str_replace('WHERE AND', 'WHERE', $query);
            
        $stmt = $this->db->prepare($query);
        $stmt->bind_param($num_params, ...$params);

        $stmt->execute();

        if($result = $stmt->get_result()) {
            return $result->fetch_all(MYSQLI_ASSOC);
        }
    }

    public function postDetection() {}


}