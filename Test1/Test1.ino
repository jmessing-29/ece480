#include <SoftwareSerial.h>
SoftwareSerial mySerial(3,2);

int pinLED = 10;
int pinPump = 5;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(pinLED, OUTPUT);
  pinMode(pinPump, OUTPUT);

  digitalWrite(pinPump, LOW);

  Serial.begin(9600); //open the serial port
  mySerial.begin(9600); // open the bluetooth serial port
}

void loop() {
  // put your main code here, to run repeatedly:
    if (mySerial.available()) 
  {
    switch (mySerial.read())
    {
      case 'x': 
        // turn on the LED
        Serial.println(F("X pressed, turn on LED for 2 seconds")); 
        mySerial.println("LED Turned On");
        digitalWrite(pinLED, HIGH);  // turn the LED on (HIGH is the voltage level)
        delay(2000);                      // wait for a second
        digitalWrite(pinLED, LOW);   // turn the LED off by making the voltage LOW
        break;
      
      case 'y':
        // turn on a pump
        Serial.println(F("Y pressed, turn on pump at 5V")); 
        digitalWrite(pinPump, HIGH);
        break;
      case 'z':
        // turn off a pump
        Serial.println(F("Z pressed, turn off pump")); 
        digitalWrite(pinPump, LOW);
        break;

      case 'a':
        // turn on a pump
        Serial.println(F("A pressed, turn on pump at 3.5V")); 
        analogWrite(pinPump, 178.5);
        break;
    }
  }
}
