#include <WiFi.h>
#include <ArduinoOTA.h>

const char* ssid = "#####";     // Replace with your WiFi network name
const char* password = "######"; // Replace with your WiFi network password


void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(23, OUTPUT);
  pinMode(22, OUTPUT);

  // Start WiFi and OTA setup
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    // digitalWrite(23, !digitalRead(23));

}

  // OTA setup
  ArduinoOTA.setHostname("myesp32"); // Set the hostname for OTA
  ArduinoOTA.onStart([]() {
    // Actions to perform when OTA update starts
  });
  ArduinoOTA.onEnd([]() {
    // Actions to perform when OTA update ends
  });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    // Actions to perform during OTA update progress
  });
  ArduinoOTA.onError([](ota_error_t error) {
    // Actions to perform on OTA update error
  });
  ArduinoOTA.begin(); // Start the OTA service
}

// the loop function runs over and over again forever
void loop() {

  ArduinoOTA.handle(); // Handle OTA updates

  digitalWrite(23, HIGH);  // turn the LED on (HIGH is the voltage level)
  delay(1000);                      // wait for a second
  digitalWrite(23, LOW);   // turn the LED off by making the voltage LOW
  delay(1000);                      // wait for a second
}
