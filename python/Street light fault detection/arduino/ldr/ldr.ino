const int ldrPin = A0;  // Analog pin connected to LDR module
const int ledPin = 7;  // Digital pin connected to LED


int ldrValue;    // Variable to store the analog reading from the LDR
int threshold = 500;  // Adjust this threshold based on your lighting conditions

void setup() {
  
  pinMode(ledPin, OUTPUT);  // Set LED pin as output
}

void loop() {
  ldrValue = analogRead(ldrPin);  // Read analog value from LDR module

  // Check if it's dark (LDR reading below threshold)
  if (ldrValue  < threshold) {
    digitalWrite(ledPin, LOW);  // Turn on LED
  } else {
    digitalWrite(ledPin, HIGH);   // Turn off LED
  }



  delay(100);  // Optional delay to avoid rapid flickering
}
