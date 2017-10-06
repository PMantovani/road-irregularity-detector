/*
 * Road Irregularity Detector
 * 
 * This program uses sensor data from an accelerometer and GPS to detect holes in roads
 * 
 * Author: Pedro Mantovani Antunes
 * Date: October 06th, 2017
 */

#include <SPI.h>
#include <Ethernet.h>
#include <TinyGPS++.h>

byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
IPAddress ip(192, 168, 1, 177);
EthernetClient client;
IPAddress server(192, 168, 1, 42);
TinyGPSPlus gps;

void setup() {
  Serial.begin(9600); // USB Serial to pins 0 and 1
  Serial3.begin(9600); // GPS Serial to pins 14 and 15
  delay(1000); // Give some time to boot up the ethernet module
  Ethernet.begin(mac, ip);
}

void loop() {

  // Fetch data from GPS
  getGpsData();
  
  // Post data to server if location found
  if(gps.location.isValid()) {
    postDetection(123, gps.location.lat(), gps.location.lng());
  }
  else {
    Serial.println("No GPS data");
  }

  // Delay to avoid multiple requests
  delay(10000);
}

void postDetection(int accelerometer, float latitude, float longitude) {
  String json = "{\"latitude\": \"@latitude\", \"longitude\": \"@longitude\","
                "\"accelerometer\": \"@accelerometer\"}";
  json.replace("@latitude", String(latitude));
  json.replace("@longitude", String(longitude));
  json.replace("@accelerometer", String(accelerometer));

  client.stop(); // close any open connections
  
  if (client.connect(server, 8080)) {
    client.println("POST api.php HTTP/1.1");
    client.println("Content-Type: application/json");
    client.println("Connection: close");
    client.println();
    client.println(json);
  }
  
  else {
    Serial.println("Connection Failed");
  }
}

void getGpsData() {
  if(Serial3.available()) {
    gps.encode(Serial3.read());
  }
}

