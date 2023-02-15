#include <Wire.h>
int receivedValues[11];
int status[5] = {1, 0, 0, 1, 1};
int counter = 0;

const int heater_relay1 = 4;
const int heater_relay2 = 5;
const int heater_relay3 = 6;
const int heater_relay4 = 7;
const int analogIn = A0;
int mVperAmp = 100; // use 100 for 20A Module and 66 for 30A Module
int RawValue= 0;
int ACSoffset = 2500;
double Voltage = 0;
double Amps = 0;

void setup() {
  pinMode(heater_relay1, OUTPUT);
  pinMode(heater_relay2, OUTPUT);
  pinMode(heater_relay3, OUTPUT);
  pinMode(heater_relay4, OUTPUT);
  /*
  for (int i=0;i<=2;i++)
  {
    digitalWrite(heater_relay1, HIGH);
    delay(70);
    digitalWrite(heater_relay2, HIGH);
    delay(70);
    digitalWrite(heater_relay3, HIGH);
    delay(70);
    digitalWrite(led_relay, HIGH);
    delay(70);
    digitalWrite(heater_relay1, LOW);
    delay(70);
    digitalWrite(heater_relay2, LOW);
    delay(70);
    digitalWrite(heater_relay3, LOW);
    delay(70);
    digitalWrite(led_relay, LOW);
    delay(70);
  }
  */
  Serial.begin(9600);
  //pinMode (ledPin, OUTPUT);
  // Start the I2C Bus as Slave on address 9
  Wire.begin(9);
  // Attach a function to trigger when something is received.
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
}
void requestEvent() {
  for (int i = 0; i < 5; i++) {
    Wire.write(status[i]);
  }
  Wire.write((int)Voltage);
  Wire.write((int)Amps);
}
void receiveEvent(int bytes) {
  while (Wire.available()) { // slave may send less than requested
    receivedValues[counter] = Wire.read();
    Serial.print(receivedValues[counter]);
    counter++;
    Serial.println(); 
    if (receivedValues[5] > receivedValues[0]) {
      digitalWrite(heater_relay1, HIGH);      
      status[0] = 0;
    }
    else {
      digitalWrite(heater_relay1, LOW); 
      status[0] = 1;       
    }  
    if (receivedValues[6] > receivedValues[1]) {
      digitalWrite(heater_relay2, HIGH); 
      status[1] = 0;     
    }
    else {
      digitalWrite(heater_relay2, LOW);  
      status[1] = 1;      
    }       
    if (receivedValues[7] > receivedValues[2]) {
      digitalWrite(heater_relay3, HIGH);
      status[2] = 0;      
    }
    else {
      digitalWrite(heater_relay3, LOW); 
      status[2] = 1;       
    }   
    if (receivedValues[8] > receivedValues[3]) {
      digitalWrite(heater_relay4, HIGH);   
      status[3] = 0;   
    }
    else {
      digitalWrite(heater_relay4, LOW);        
      status[3] = 1;
    }                
  }
  counter = 0;
  
}
void loop() {
  RawValue = analogRead(analogIn);
  Voltage = (RawValue / 1024.0) * 5000; // Gets you mV
  Amps = ((Voltage - ACSoffset) / mVperAmp);  
  delay(2000);
}
