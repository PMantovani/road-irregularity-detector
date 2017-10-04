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

$mysqli = new mysqli("localhost", "road", "road-mysql", "roadmanager");

if ($method === "POST") {
    $query = "INSERT INTO detections (position, reading_value, reading_date) VALUES (?, ?, NOW());";

    if ($stmt = $mysqli->prepare($query)) {

        $stmt->bind_param("ss", $input_json["position"], $input_json["reading_value"]);
        $stmt->execute();
        $stmt->close();
    }

    echo "success";
}
else if ($method === "GET") {
    $query = "SELECT * FROM detections;";

    if($result = $mysqli->query($query)) {
        $allRows = $result->fetch_all(MYSQLI_ASSOC);
        $json = json_encode($allRows);
        $result->close();
        echo $json;
    }
}

$mysqli->close();