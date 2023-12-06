#include <SoftwareSerial.h>
#include <Adafruit_MCP4725.h>
#include <Wire.h>

#define analogVin A0
#define potentioVin A2

#define pinLED 100  // undefined, potentially unneccessary
#define pinPump 10
#define pinSwitch 9
#define pinRead 8

const int pinSweep = 6;

SoftwareSerial mySerial(3,2);

Adafruit_MCP4725 dac;

enum stateP {pumping, OFF} pump_state;
enum stateS {not_sweeping, sweeping} sweep_state;
enum stateBt {no_con, con_send, con_no_send} bt_state;
enum stateSw {goingUp, goingDown} sweeping_state;
// common abreviation, bt = BlueTooth
bool flushing = false;

float pot_output = 0.0;
int send_data_delay = 250;  // value that will change how many loops we wait to send data
int voltage = 0;
String bt_msg = "";

void setup() {
  // put your setup code here, to run once:
  pinMode(pinLED, OUTPUT);
  pinMode(pinPump, OUTPUT);
  pinMode(pinSwitch, OUTPUT);

  digitalWrite(pinPump, LOW);
  digitalWrite(pinSwitch, LOW);

  dac.begin(0x60);

  Serial.begin(9600); // open the arduino serial monitor port
  mySerial.begin(9600); // open the bluetooth serial port

  pump_state = OFF;  // pumps start in OFF state, not pumping
  bt_state = no_con;  // bt starts with no connection
  sweep_state = not_sweeping;
  sweeping_state = goingUp;
}

void loop() {
  // put your main code here, to run repeatedly:
  // avoiding use of delays, since that will mess with the state machine
  // instead use counters

  // Collect an Instruction from the User via Py via BT
  // Control the state of operations based on that instruction
  if (mySerial.available()){
    bt_msg = mySerial.read();

    if (bt_msg == "start sweep"){
      sweep_state = sweeping;
    }
    if (bt_msg == "stop sweep"){
      sweep_state = not_sweeping;
      voltage = 0;  // so when a new sweep starts, it starts at the bottom of the sweep
    }
    if (bt_msg == "start pump"){
      pump_state = pumping;
      digitalWrite(pinPump, HIGH);
    }
    if (bt_msg == "stop pump"){
      pump_state = OFF;
      digitalWrite(pinPump, LOW);
    }
    if (bt_msg == "switch pump"){
      if(not flushing){
        flushing = true;
        digitalWrite(pinSwitch, HIGH);
      }
      else{
        flushing = false;
        digitalWrite(pinSwitch, LOW);
      }
    }
  }
  // voltage sweep controlled by the arduino
  // voltage divided by 819 is the actual voltage value
  if (sweep_state == sweeping){
    if (voltage <= 4095 && voltage >= 0){
      if(sweeping_state == goingUp){
        voltage += 10;
        dac.setVoltage(voltage, false);
      }
      else if(sweeping_state == goingDown){
        voltage -= 10;
        dac.setVoltage(voltage, false);
      }
    }
    else if(voltage >= 4095){
      sweeping_state = goingDown;
      voltage = 4095;
      Serial.println("**********CHANGING DIRECTION**********");
    }
    else if(voltage <= 0){
      sweeping_state = goingUp;
      voltage = 0;
      Serial.println("**********CHANGING DIRECTION**********");
    }
    Serial.println(voltage);
    Serial.println(sweeping_state);
  }

  // send the data back to Py, if its receiving
  if (mySerial.available()){
    // send data from the pin, and the votage
    
  }



}
