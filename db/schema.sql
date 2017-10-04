CREATE DATABASE IF NOT EXISTS roadmanager;

USE roadmanager;

CREATE TABLE IF NOT EXISTS detections (
  id                BIGINT(12) UNSIGNED AUTO_INCREMENT,
  sensor_id         BIGINT(12) UNSIGNED,
  position          VARCHAR(50) NOT NULL,
  reading_value     INT NOT NULL,
  reading_date      DATETIME,
  PRIMARY KEY (id)
);