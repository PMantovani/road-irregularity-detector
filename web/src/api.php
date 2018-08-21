<?php
/**
 * User: Pedro Mantovani Antunes
 * Date: 04-Oct-17
 * Time: 2:40 PM
 */

require_once('RoadManagerDB.php');
require_once('RoadsGoogleApi.php');

$method = $_SERVER['REQUEST_METHOD'];
$path = explode('/', trim($_SERVER['PATH_INFO'],'/'))[0];
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

$roadManagerDb = new RoadManagerDB();

if ($method === "POST") {
    $id = $roadManagerDb->insertDetection($input_json);
    $roadManagerDb->insertDetectionPath($id, $input_json['start_latitude'], $input_json['start_longitude'],
                                             $input_json['end_latitude'],   $input_json['end_longitude']);

    http_response_code(201);
    echo $id;
}


else if ($method === "GET") {
    if ($path === 'detections') {
        $output = $roadManagerDb->getDetections($_GET);
    }
    else if ($path === 'sensors') {
        $output = $roadManagerDb->getSensors();
    }

    $json = json_encode($output);
    header("Content-Type: application/json");
    echo $json;
}