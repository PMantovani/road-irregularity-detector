CREATE DATABASE IF NOT EXISTS roadmanager;

USE roadmanager;

CREATE TABLE IF NOT EXISTS detections (
  id                BIGINT(12) UNSIGNED AUTO_INCREMENT,
  sensor_id         BIGINT(12) UNSIGNED,
  latitude          FLOAT(11,8) NOT NULL,
  longitude         FLOAT(11,8) NOT NULL,
  st_number         VARCHAR(100),
  street            VARCHAR(100),
  city              VARCHAR(100),
  state             VARCHAR(100),
  country           VARCHAR(100),
  speed             FLOAT(5,2),
  course            SMALLINT,
  accelerometer     FLOAT(5,3) NOT NULL,
  reading_date      DATETIME,
  created_date      DATETIME,
  PRIMARY KEY (id)
) CH;