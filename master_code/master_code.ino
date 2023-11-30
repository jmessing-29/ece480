#include <SoftwareSerial.h>
#include <Adafruit_MCP4725.h>
#include <Wire.h>

#define analogVin A0
#define potentioVin A2

#define pinLED 100  // undefined, potentially unneccessary
#define pinPump 10
#define pinSwitch 9

SoftwareSerial mySerial(3,2);

Adafruit_MCP4725 dac;

enum stateP {pumping, flushing, OFF} pump_state;
enum stateS {not_sweeping, sweeping} sweep_state;
enum stateBt {no_connection, con_send, con_no_send} bt_state;
// common abreviation, bt = BlueTooth
float pot_output = 0.0;
int send_data_delay = 250;  // value that will change how many loops we wait to send data

void setup() {
  // put your setup code here, to run once:
  pinMode(pinLED, OUTPUT);
  pinMode(pinPump, OUTPUT);

  digitalWrite(pinPump, LOW);
  digitalWrite(pinSwitch, LOW);

  dac.begin(0x60);

  Serial.begin(9600); // open the arduino serial monitor port
  mySerial.begin(9600); // open the bluetooth serial port

  pump_state = OFF;  // pumps start in OFF state, not pumping
  bt_state = no_connection;  // bt starts with no connection
}

void loop() {
  // put your main code here, to run repeatedly:
  // avoiding use of delays, since that will mess with the state machine
  // instead use counters



}
