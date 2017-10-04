<?php
/**
 * User: Pedro Mantovani Antunes
 * Date: 04-Oct-17
 * Time: 2:40 PM
 */

$method = $_SERVER['REQUEST_METHOD'];
$input = file_get_contents('php://input');
$input = json_decode($input, true);

if ($method === "POST") {
    $mysqli = new mysqli("localhost", "road", "road-mysql", "roadmanager");
    $query = "INSERT INTO detections (position, reading_value, reading_date) VALUES (?, ?, NOW());";

    if ($stmt = $mysqli->prepare($query)) {

        $stmt->bind_param("ss", $input["position"], $input["reading_value"]);
        $stmt->execute();
        $stmt->close();
    }
}
else if ($method === "GET") {

}