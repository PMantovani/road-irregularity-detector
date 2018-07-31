CREATE DATABASE IF NOT EXISTS roadmanager;

USE roadmanager;

CREATE TABLE IF NOT EXISTS detections (
  id                BIGINT(12) UNSIGNED AUTO_INCREMENT,
  sensor_id         BIGINT(12) UNSIGNED,
  start_latitude    FLOAT(11,8) NOT NULL,
  start_longitude   FLOAT(11,8) NOT NULL,
  end_latitude      FLOAT(11,8) NOT NULL,
  end_longitude     FLOAT(11,8) NOT NULL,
  speed             FLOAT(5,2),
  course            SMALLINT,
  quality           SMALLINT NOT NULL,
  reading_date      DATETIME NOT NULL,
  created_date      DATETIME NOT NULL,
  PRIMARY KEY (id)
);