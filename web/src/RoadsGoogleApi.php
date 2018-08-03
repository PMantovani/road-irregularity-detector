<?php

require_once('MissingFieldsException.php');

class RoadsGoogleApi {

    const key = "AIzaSyCaJlQ4XP8Pl0oOp5JO9YqfyvyDaTg00eg";
    const mainUrl = "https://roads.googleapis.com/v1/snapToRoads";

    public function snapToRoads(float $start_lat, float $start_lng, float $end_lat, float $end_lng) {
        
        $fullUrl = self::mainUrl .
            '?path=' . $start_lat . ',' . $start_lng . '|' . $end_lat . ',' . $end_lng .
            '&interpolate=true' .
            '&key=' . self::key;

        $response = file_get_contents($fullUrl);
        return json_decode($response, true);
    }
}