#include <SoftwareSerial.h>
#include <Adafruit_MCP4725.h>
#include <Wire.h>

#define analogVin A0
#define potentioVin A2

SoftwareSerial mySerial(3,2);

int pinLED = 10;
int pinPump = 5;

int stateLED = 0;
int statePotentioRead = 0;

Adafruit_MCP4725 dac;

void setup() {
  // put your setup code here, to run once:
  // Serial.begin(9600);

  pinMode(pinLED, OUTPUT);
  pinMode(pinPump, OUTPUT);

  digitalWrite(pinPump, LOW);

  dac.begin(0x60);

  Serial.begin(9600);
  mySerial.begin(9600); // open the bluetooth serial port
}

void loop() {
  // put your main code here, to run repeatedly:
  float output = analogRead(potentioVin);
  Serial.println("Voltage read: "); Serial.println(output * 0.0049);
  delay(250);

  if (mySerial.available()) 
  {
    switch (mySerial.read())
    {
      case 'x': 
        // turn on the LED
        Serial.println(F("X pressed, turn on LED")); 
        
        digitalWrite(pinLED, HIGH);  // turn the LED on (HIGH is the voltage level)

        mySerial.println("LED Turned On");
        break;
      case 'b':
        Serial.println(F("B pressed, turn off LED"));
        digitalWrite(pinLED, LOW);   // turn the LED off by making the voltage LOW

        mySerial.println(F("LED Turned Off"));
        break;
      case 'y':
        // turn on a pump
        Serial.println(F("Y pressed, turn on pump at 5V")); 
        dac.setVoltage((5*4095)/5, false);
        break;
      case 'z':
        // turn off a pump
        Serial.println(F("Z pressed, turn off pump")); 
        dac.setVoltage((0*4095)/5, false);
        break;

      case 'a':
        // turn on a pumpz
        Serial.println(F("A pressed, turn on pump at 3.5V")); 
        dac.setVoltage((3.5*4095)/5, false);
        break;
    }
  }
}
