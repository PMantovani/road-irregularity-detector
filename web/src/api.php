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
    $query = "INSERT INTO detections (latitude, longitude, accelerometer, reading_date) VALUES (?, ?, ?, NOW());";

    if ($stmt = $mysqli->prepare($query)) {

        $stmt->bind_param("ssss", $input_json["latitude"], $input_json["longitude"],
            $input_json["accelerometer"], $input_json["speed"], $input_json["reading_date"]);
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