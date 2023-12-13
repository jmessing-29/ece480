#include <SoftwareSerial.h>
#include <Adafruit_MCP4725.h>
#include <Wire.h>

#define potentioVin A3

#define pinPump 9
#define pinSwitch 10


const int pinSweep = 6;

SoftwareSerial mySerial(3,2);

Adafruit_MCP4725 dac;

enum stateP {pumping, OFF} pump_state;
enum stateS {not_sweeping, sweeping} sweep_state;
enum stateBt {no_con, con_send, con_no_send} bt_state;
enum stateSw {goingUp, goingDown} sweeping_state;

// enum stateSq {start, stop, loopSweep, flush} sequence_state;
// common abreviation, bt = BlueTooth
int sequence_state = 0;
bool flushing = false;

const unsigned long interval_start = 2000;
unsigned long counter_start = 0;

unsigned long counter_loop = 0;

unsigned long counter_send = 0;

const unsigned long interval_flush = 1000; // 10000 is 1 minute
unsigned long counter_flush = 0;

const unsigned long interval_high = 500;
const unsigned long interval_low = 125;


float pot_output = 0.0;
int send_data_delay = 250;  // value that will change how many loops we wait to send data
int voltage = 0;
//String bt_msg = "";

// a full reset to the board state
void stop_everything(){
  digitalWrite(pinPump, HIGH);
  digitalWrite(pinSwitch, HIGH);

  counter_start = 0;
  counter_loop = 0;
  counter_flush = 0;
  voltage = 0;
}

void setup() {
  // put your setup code here, to run once:
  pinMode(pinPump, OUTPUT);
  pinMode(pinSwitch, OUTPUT);

  digitalWrite(pinPump, HIGH);
  digitalWrite(pinSwitch, HIGH);

  dac.begin(0x60);

  Serial.begin(9600); // open the arduino serial monitor port
  mySerial.begin(9600); // open the bluetooth serial port

  pump_state = OFF;  // pumps start in OFF state, not pumping
  bt_state = no_con;  // bt starts with no connection
  sweep_state = not_sweeping;
  sweeping_state = goingUp;

  sequence_state = 0;
}

void loop() {
  // put your main code here, to run repeatedly:
  // avoiding use of delays, since that will mess with the state machine
  // instead use counters

  // Collect an Instruction from the User via Py via BT
  // Control the state of operations based on that instruction

  if (mySerial.available() > 0){
    auto bt_msg = mySerial.read();

    Serial.println(bt_msg);

    // start sequence key
    if (bt_msg == 97){
      Serial.println("Start message received");
      sequence_state = 1;
    }
    // stop sequence key
    else if (bt_msg == 98){
      Serial.println("Stop message received");
      sequence_state = 0;

      stop_everything();
    }
    // reset, flush key
    else if (bt_msg == 99){
      Serial.println("Flush message received");

      digitalWrite(pinSwitch, LOW);

      sequence_state = 3;
    }

  }
  // voltage sweep controlled by the arduino
  // voltage divided by 819 is the actual voltage value
  if (sequence_state == 1){
    // Pump for interval_start
    if (counter_start++ <= interval_start){
      digitalWrite(pinPump, LOW);
    }
    else{
      sequence_state = 2;
      counter_start = 0;
    }
  }

  // The sweeping loop
  // responsible for voltage sweep, oscilating pump, and sending data read from pot stat
  if (sequence_state == 2){
    if(counter_send++ <= 15){
      Serial.println("****************SENT SOMETHING*******************");
      mySerial.print(voltage/819.0);
      mySerial.print(",");
      mySerial.println(analogRead(potentioVin));

      //mySerial.print(random(0,50));
      //mySerial.print(",");
      //mySerial.println(random(50,100));

      counter_send = 0;
    }

    if(counter_loop >= interval_high){
      counter_loop = 0;
    }
    else if(counter_loop++ <= interval_low){
      digitalWrite(pinPump, LOW);
    }
    else if(counter_loop > interval_low){
      digitalWrite(pinPump, HIGH);
    }
    else{
      digitalWrite(pinPump, HIGH);
    }
    Serial.println(counter_loop);

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
  }


  if(sequence_state == 3){
    if (counter_flush++ <= interval_flush){
      digitalWrite(pinPump, LOW);

      Serial.println(counter_flush);
    }
    else{
      sequence_state = 0;

      stop_everything();
    }
  }
}
