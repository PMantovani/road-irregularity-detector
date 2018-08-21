CREATE DATABASE IF NOT EXISTS roadmanager;

USE roadmanager;

CREATE TABLE IF NOT EXISTS sensors (
  id         BIGINT(12) UNSIGNED AUTO_INCREMENT,
  name       VARCHAR(50),
  last_seen  DATETIME NOT NULL,
  last_lat   FLOAT(11,8),
  last_lng   FLOAT(11,8),
  created_on DATETIME NOT NULL,
  PRIMARY KEY (id)
);

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
  PRIMARY KEY (id),
  FOREIGN KEY (sensor_id) 
    REFERENCES sensors(id) 
    ON DELETE CASCADE
    ON UPDATE CASCADE 
);

CREATE TABLE IF NOT EXISTS detections_path (
  id            BIGINT(12) UNSIGNED AUTO_INCREMENT,
  detection_id  BIGINT(12) UNSIGNED,
  path_counter  BIGINT(12) UNSIGNED NOT NULL,
  latitude      FLOAT(11,8) NOT NULL,
  longitude     FLOAT(11,8) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (detection_id, path_counter),
  FOREIGN KEY (detection_id) 
    REFERENCES detections(id) 
    ON DELETE CASCADE
    ON UPDATE CASCADE 
);