CREATE DATABASE IF NOT EXISTS roadmanager;

USE roadmanager;

CREATE TABLE IF NOT EXISTS detections (
  id                BIGINT(12) UNSIGNED AUTO_INCREMENT,
  sensor_id         BIGINT(12) UNSIGNED,
  latitude          FLOAT(11,8) NOT NULL,
  longitude         FLOAT(11,8) NOT NULL,
  accelerometer     INT NOT NULL,
  reading_date      DATETIME,
  PRIMARY KEY (id)
);