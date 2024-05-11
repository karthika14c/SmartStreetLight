const int ldrPin = A0;  // LDR analog pin
const int sensorPin = A1;  // LM35 sensor analog pin
const int voltagePin = A2;  // Voltage sensor analog pin
unsigned int IRpin = 3; // IR receiver digital pin
const int ledPin = 7;  // LED digital pin

int ldrValue, watts;
char set =  '2';
float voltage, temperature, temperaturefr, current;
int threshold = 500;  // adjust based on your LDR sensitivity in dark conditions


void setup() {
  pinMode(IRpin, INPUT_PULLUP);
  Serial.begin(9600);       // Initialize serial communication
  pinMode(ledPin, OUTPUT);
  
}

void loop() {

  ldrValue = analogRead(ldrPin);  // Read analog value from LDR module
  char command;

  if (Serial.available() > 0) {  // Check if data is available to read
    command = Serial.read(); // Read the incoming command
    if (command == '1')  {
      set = '1'; //Set Light ON until next input
    }
    else if (command == '0') {
      set = '0';
    }
    else if (command == '2'){
      set = '2';
    }
  }


  if ( (digitalRead(IRpin) == LOW) or (set == '1')) {
    
    digitalWrite(ledPin, HIGH); // Turn on the light
  
  }
  // else if ((ldrValue > threshold) or (digitalRead(IRpin) == LOW)) {
    
  //   digitalWrite(ledPin, HIGH); // Turn on the light
  
  // }  
  else {
    digitalWrite(ledPin, LOW);   // Turn off LED
  }

  // this condition is always bottom so it perform manual operation 
  if (set == '0') {
    digitalWrite(ledPin, LOW);  // Turn off LED
  }


  // Read voltage from sensor (adjust for your voltage divider setup)
  int voltageValue = analogRead(voltagePin);
  voltage = (voltageValue * 5.0) / 1023.0;  // Assuming 5V reference and 10-bit ADC
  current = (voltageValue - 2.5) / 0.1;
  current = current / 1000;
  watts = current * voltage;
  // Read raw ADC value from LM35
  int temparatureValue = analogRead(sensorPin);

  // Convert ADC value to temperature in Celsius
  temperature = (temparatureValue - 32)* 0.5;  // LM35 outputs 10mV/°C
  
// Fahrenhit
 // temperaturefr = (temparatureValue * 1.8) + 32;
  int pinValue = digitalRead(ledPin);
  int IRValue = digitalRead(IRpin);


  // Print readings to serial monitor
  Serial.print("Device_Name: ");
  Serial.print("Light1");
  Serial.print(",");
  Serial.print("LED_Voltage: ");
  Serial.print(voltage);
  Serial.print(",");
  Serial.print("LED_Current: ");
  Serial.print(current);
  Serial.print(",");
  Serial.print("LED_Watts: ");
  Serial.print(watts);
  Serial.print(",");
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(",");
  Serial.print("Temperature2: ");
  Serial.print(temparatureValue);
  Serial.print(",");
  Serial.print("Light_Density: ");
  Serial.print(ldrValue);
  Serial.print(",");
  Serial.print("Light_PIN: ");
  Serial.print(pinValue);
  Serial.print(",");
  Serial.print("Input: ");
  Serial.print(set);
  Serial.print(",");
  Serial.print("IR: ");
  Serial.print(IRValue);
  Serial.println("");
  

  delay(3000);  // Optional delay to avoid rapid flickering
} 
