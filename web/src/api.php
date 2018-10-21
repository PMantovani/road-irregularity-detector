<?php
/**
 * User: Pedro Mantovani Antunes
 * Date: 04-Oct-17
 * Time: 2:40 PM
 */

require_once('RoadManagerDB.php');
require_once('RoadsGoogleApi.php');
require_once('MissingFieldsException.php');

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
    try {
        for ($i=0; $i<sizeof($input_json); $i++) {
            
            $id = $roadManagerDb->insertDetection($input_json[$i]);
            $roadManagerDb->insertDetectionPath($id, $input_json[$i]['start_latitude'], $input_json[$i]['start_longitude'],
                                                    $input_json[$i]['end_latitude'],   $input_json[$i]['end_longitude']);
        }
        
        http_response_code(201);
        echo $id;
    } catch (MissingFieldsException $e) {
        http_response_code(400);
        echo $e->getMessage();
    }
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