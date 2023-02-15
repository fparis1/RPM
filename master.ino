
//Include DHT Library
#include <dht11.h>
#include <string.h>
#include <Wire.h>
//Initialise DHT Library and define data pin
dht11 DHT;
#define DHT11_PIN 4 
#define LM35DZ_PIN A0
#define VMA320_PIN_1 A1
#define VMA320_PIN_2 A2
#define VMA328_PIN A3

int ref[5];
String incomingByte = "";
char buff[50];
int statusHeaterLED[8];
int counter = 0;
void setup()
{
  Serial.begin(9600);  
  Wire.begin();
}

void loop()
{
         

  if (Serial.available()) {

    incomingByte = Serial.readString(); //112-12-12-12-2
    incomingByte.toCharArray(buff, 50);
    
    char *token = strtok(buff, "-");
    // loop through the string to extract all other tokens
    int i = 0;
    while( token != NULL ) {
        ref[i] = atoi(token);
        token = strtok(NULL, "-");
        i++;
    } 
     
  }
  else {
    int chk = DHT.read(DHT11_PIN);
    int reading = analogRead(LM35DZ_PIN);
    int reading2 = analogRead(VMA320_PIN_1);
    int reading3 = analogRead(VMA320_PIN_2);
    int reading4 = analogRead(VMA328_PIN);
    
    float voltage = reading * (5.0 / 1023.0);    
    float tempLM35DZ = voltage * 100;

    float tempVMA320_1 = ((reading2 * 5.0) / 1024.0) * 10;
    float tempVMA320_2 = ((reading3 * 5.0) / 1024.0) * 10;
    
    float tempDHT = DHT.temperature;
    float humDHT = DHT.humidity;
    
    Wire.beginTransmission(9);
    Wire.write(ref[0]);
    Wire.write(ref[1]);
    Wire.write(ref[2]);
    Wire.write(ref[3]);
    Wire.write(ref[4]);
    Wire.write((int)tempDHT);
    Wire.write((int)humDHT);
    Wire.write(reading4);
    Wire.write((int)tempLM35DZ);
    Wire.write((int)tempVMA320_1);
    Wire.write((int)tempVMA320_2);
    Wire.endTransmission(); 
    
    Wire.requestFrom(9, 7);   
    while(Wire.available()) {
     statusHeaterLED[counter] = Wire.read();
     counter++;
    }
    counter = 0;
    //Print temp and hum values onto serial monitor
    //x is used as a delimiter
    Serial.print(tempDHT);
    Serial.print("x");
    Serial.print(humDHT);
    Serial.print("x");
    Serial.print(reading4);
    Serial.print("x");
    Serial.print(tempLM35DZ);
    Serial.print("x");
    Serial.print(tempVMA320_1);
    Serial.print("x");
    Serial.print(tempVMA320_2);
    Serial.print("x");
    Serial.print(statusHeaterLED[0]);
    Serial.print("x");
    Serial.print(statusHeaterLED[1]);
    Serial.print("x");
    Serial.print(statusHeaterLED[2]);
    Serial.print("x");
    Serial.print(statusHeaterLED[3]);
    Serial.print("x");
    Serial.print(statusHeaterLED[4]);
    Serial.print("x");
    Serial.print(statusHeaterLED[5]);
    Serial.print("x");
    Serial.print(statusHeaterLED[6]);
    Serial.print("x");
    Serial.print(statusHeaterLED[7]);    
    Serial.println("x");
    delay(2000);  
  }

}

