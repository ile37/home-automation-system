
const int LED_RED_PIN = 22; // Example pin for the red LED
const int LED_BLUE_PIN = 23; // Example pin for the blue LED


void callback(char* topic, byte* payload, unsigned int length) {
    // Convert the incoming byte array to a string
    String message;
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];
    }

    // Check the message and act accordingly
    if (message == "red_on") {
        digitalWrite(LED_RED_PIN, HIGH);
    } else if (message == "red_off") {
        digitalWrite(LED_RED_PIN, LOW);
    } else if (message == "blue_on") {
        digitalWrite(LED_BLUE_PIN, HIGH);
    } else if (message == "blue_off") {
        digitalWrite(LED_BLUE_PIN, LOW);
    }
}


void setup() {
  pinMode(LED_RED_PIN, OUTPUT);
  pinMode(LED_BLUE_PIN, OUTPUT);
}


void loop() {
}
