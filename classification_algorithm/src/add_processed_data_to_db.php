<?php

$file = fopen('..\..\data\processed_data.csv', 'r');

$firstLine = true;

$mysqli = new mysqli("localhost", "root", "root12mysql!", "roadmanager");

while (($row = fgetcsv($file, 1000)) !== NULL) {
    if ($firstLine) {
        $firstLine = false;
        continue;
    }

    $query = "INSERT INTO detections (start_latitude, start_longitude, end_latitude, end_longitude, quality) 
              VALUES (?, ?, ?, ?, ?);";

    if ($stmt = $mysqli->prepare($query)) {
        $stmt->bind_param("sssss", $row[15], $row[16], $row[17], $row[18], $row[0]);
        $stmt->execute();
    }
}