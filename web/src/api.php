<?php
/**
 * User: Pedro Mantovani Antunes
 * Date: 04-Oct-17
 * Time: 2:40 PM
 */

$method = $_SERVER['REQUEST_METHOD'];
$input = file_get_contents('php://input');
$input_json = json_decode($input, true);

if (empty($input_json) && $method === "POST") {
    http_response_code(400);
    exit();
}
else if($method !== "GET" && $method !== "POST") {
    http_response_code(405);
    exit();
}

$mysqli = new mysqli("localhost", "road", "road-mysql", "roadmanager");

if ($method === "POST") {
    $query = "INSERT INTO detections (latitude, longitude, accelerometer, speed, reading_date, st_number, street,
              city, state, country, created_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW());";

    if ($stmt = $mysqli->prepare($query)) {
        $st_number = $street = $city = $state = $country = null;
        $latlng = $input_json["latitude"] . ',' . $input_json["longitude"];
        $key = "AIzaSyCaJlQ4XP8Pl0oOp5JO9YqfyvyDaTg00eg";

        $response = file_get_contents("https://maps.googleapis.com/maps/api/geocode/json?latlng=" .
                                        $latlng . "&key=" . $key);
        $address_json = json_decode($response, true);
        if ($address_json["status"] === "OK" && count($address_json["results"]) > 0) {
            foreach ($address_json["results"][0]["address_components"] as $components) {
                if (in_array("street_number", $components["types"])) {
                    $st_number = $components["short_name"];
                }
                if (in_array("route", $components["types"])) {
                    $street = $components["short_name"];
                }
                if (in_array("locality", $components["types"])) {
                    $city = $components["short_name"];
                }
                if (in_array("administrative_area_level_1", $components["types"])) {
                    $state = $components["long_name"];
                }
                if (in_array("country", $components["types"])) {
                    $country = $components["long_name"];
                }
            }
        }

        $stmt->bind_param("ssssssssss", $input_json["latitude"], $input_json["longitude"],
            $input_json["accelerometer"], $input_json["speed"], $input_json["reading_date"],
            $st_number, $street, $city, $state, $country);
        $stmt->execute();
        $stmt->close();
    }

    http_response_code(201);
}
else if ($method === "GET") {
    $query = "SELECT * FROM detections;";

    if($result = $mysqli->query($query)) {
        $allRows = $result->fetch_all(MYSQLI_ASSOC);
        $json = json_encode($allRows);
        $result->close();
        header("Content-Type: application/json");
        echo $json;
    }
}

$mysqli->close();