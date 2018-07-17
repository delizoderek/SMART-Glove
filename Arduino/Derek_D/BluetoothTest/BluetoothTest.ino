#include "SoftwareSerial.h"
SoftwareSerial serial_connection(10,11);
#define BUFFER_SIZE 64
char inData[BUFFER_SIZE];
char inChar = -1;
int count = 0;
int i = 0;

void setup(){
  Serial.begin(9600);
  serial_connection.begin(9600);
  serial_connection.println("Ready!!!");
  Serial.println("Started");
  
}

void loop(){
  byte byte_count = serial_connection.available();
  if(byte_count){
    Serial.println("Incoming Data");
    int first_bytes = byte_count;
    int remaining_bytes = 0;
    if(first_bytes >= BUFFER_SIZE-1){
      remaining_bytes = byte_count - (BUFFER_SIZE - 1);
    }
    for(i = 0; i < first_bytes; i++){
      inChar = serial_connection.read();
      inData[i] = inChar;
    }
    inData[i] = '\0';
    for(i = 0; i < remaining_bytes; i++){
      inChar = serial_connection.read();
    }
    Serial.println(inData);
    serial_connection.println("Hello from Bluetooth " + String(count));
    count++;
  }
  delay(100);
}

