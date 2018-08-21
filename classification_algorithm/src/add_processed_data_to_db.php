<?php

require_once('../../web/src/RoadManagerDB.php');

$api = new RoadManagerDB();

$file = fopen('..\..\data\processed_data.csv', 'r');
$firstLine = true;
$counter = 0;

while (($row = fgetcsv($file, 1000)) !== NULL) {
    if ($firstLine) {
        $firstLine = false;
        continue;
    }

    $data = [];
    $data['sensor_id'] = 1;
    $data['start_latitude'] = $row[15];
    $data['start_longitude'] = $row[16];
    $data['end_latitude'] = $row[17];
    $data['end_longitude'] = $row[18];
    $data['speed'] = $row[13];
    $data['course'] = 13;
    $data['quality'] = $row[0];
    $data['reading_date'] = date('c', $row[19]);

    $id = $api->insertDetection($data);
    $api->insertDetectionPath($id, $data['start_latitude'], $data['start_longitude'], 
                                   $data['end_latitude'], $data['end_longitude']);
    
    echo $counter . ' ';
    $counter++;
    // sleep(0.12);
}