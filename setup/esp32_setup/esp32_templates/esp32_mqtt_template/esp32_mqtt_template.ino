// Start of MQTT global
#include <WiFi.h>
#include <PubSubClient.h>

const char* mqtt_server = "mqtt_server_ip"; // Replace with your MQTT server address
const int mqtt_port = 1883;
const char* mqtt_topic = "temp/temp";

WiFiClient espClient;
PubSubClient client(espClient);

void reconnect() {
    // Loop until we're reconnected
    while (!client.connected()) {
        if (client.connect("ESP32Client")) {
            // Once connected, subscribe to the topic
            client.subscribe(mqtt_topic);
        } else {
            delay(5000);
        }
    }
}
// End of MQTT global

void setup() {
  // Start of MQTT void setup
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  // End of MQTT void setup
}


void loop() {
  // Start of MQTT void loop
  if (!client.connected()) {
      reconnect();
  }
  client.loop();
  // End of MQTT void loop
}
