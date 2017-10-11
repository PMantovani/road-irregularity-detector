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
IPAddress ip(192, 168, 25, 177);
EthernetClient client;
IPAddress server(192, 168, 25, 22);
//byte server[] = {192, 168, 25, 18};
TinyGPSPlus gps;

void setup() {
  delay(1000); // Give some time to boot up the ethernet module
  
  Serial.begin(9600); // USB Serial to pins 0 and 1
  Serial3.begin(9600); // GPS Serial
  
  //Ethernet.begin(mac, ip);
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to start Ethernet module");
  }
  else {
    Serial.print("Started at ");
    Serial.println(Ethernet.localIP());
  }
  
}

void loop() {

  // Fetch data from GPS
  getGpsData();
  
  // Post data to server if location found
  if(gps.location.isValid()) {
    //printDetectionToSerial();
    //postDetection(123, gps.location.lat(), gps.location.lng(), gps.course.deg(), gps.speed.kmph());
  }
  else {
    Serial.println("No GPS data");
    //postDetection(123, gps.location.lat(), gps.location.lng(), gps.course.deg(), gps.speed.kmph());
  }

  // Delay to avoid multiple requests
  smartDelay(10000);
}

void printDetectionToSerial() {
  Serial.println("*** BURACO DETECTADO ***");
  Serial.print("Localizacao: ");
  Serial.print(gps.location.lat());
  Serial.print(",");  Serial.print(gps.location.lng());
  Serial.print("   Curso (graus): ");
  Serial.print(gps.course.deg());
  Serial.print("   Velocidade (km/h): ");
  Serial.print(gps.speed.kmph());
  Serial.print("   Acelerometro: ");
  Serial.println("123");
  Serial.println(); 
}

void postDetection(int accelerometer, float latitude, float longitude, float course, float speed) {
  String json = "{\"latitude\": \"@latitude\", \"longitude\": \"@longitude\", "
                "\"course\": \"@latitude\", \"speed\": \"@speed\", \"accelerometer\": \"@accelerometer\"}";
  json.replace("@latitude", String(latitude));
  json.replace("@longitude", String(longitude));
  json.replace("@accelerometer", String(accelerometer));
  json.replace("@course", String(course));
  json.replace("@speed", String(speed));

  client.stop(); // close any open connections
  
  if (client.connect(server, 8080)) {
    Serial.print("Connected to server!");
    String request = "POST /api.php HTTP/1.1\r\n";
    request += "Host: 192.168.25.22:8080\r\n";
    request += "Content-Type: application/json\r\n";
    request += "Content-Length: ";
    request += json.length();
    request += "\r\n\r\n";
    request += json;
    
    client.println(request);
   /* client.println();
    client.println();
    client.println();
    client.println();
    client.print();
    client.println(json.length()+1);
    client.println();
    client.print(json);*/
  }
  
  else {
    Serial.println("Connection Failed");
  }
}

void getGpsData() {
  while(Serial3.available()) {
    gps.encode(Serial3.read());
  }
}

static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (Serial3.available())
      gps.encode(Serial3.read());
    while (Serial.available()) {
      Serial.read();
      Serial.read();
      postDetection(123, gps.location.lat(), gps.location.lng(), gps.course.deg(), gps.speed.kmph());
    }
    while (client.available()) {
      char c = client.read();
      Serial.print(c);
    }
  } while (millis() - start < ms);
}
