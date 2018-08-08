/*
   Created by Derek DeLizo
   TX -> D2
   RX -> D3
*/
#include <SoftwareSerial.h>
#include<Wire.h>
#include "I2Cdev.h"
#include "MPU6050.h"

MPU6050 accelgyro;

const int MPU_addr = 0x68; // I2C address of the MPU-6050
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;
int16_t xAccelOff, yAccelOff, zAccelOff, xGyroOff, yGyroOff, zGyroOff;
float samples;
int baudrate = 9600;
int i = 0;
bool isLinked;
bool isCalibrating;
bool isTransmitting;
bool originaTap;
int pressStrength;
SoftwareSerial mySerial(2, 3);

void setup()
{
  Serial.begin(baudrate);
  mySerial.begin(baudrate);
  Serial.println("Intializing IMU");
  accelgyro.initialize();
  Serial.println("Testing Connections");
  Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
  isTransmitting = false;
  isCalibrating = false;
  samples = 500;
}

void loop()
{
  if (isTransmitting) {
    //mySerial.write("A");
    SendData();
  }

  if (isCalibrating) {
    if (samples <= 0) {
      Serial.println("Calibration Complete");
      mySerial.write('d');
      isTransmitting = true;
      isCalibrating = false;
    } else {
      samples--;
      Serial.println(samples);
      mySerial.write('c');
    }
  }

  if (mySerial.available()) {
    char in = mySerial.read();
    if (in == 'g') {
      Serial.println("Connected");
      mySerial.write('c');
      isCalibrating = true;
    }
  }

  delay(10);
}

void SendData() {
  float AcXCal, AcYCal, AcZCal, GyXCal, GyYCal, GyZCal;
  accelgyro.getMotion6(&AcX, &AcY, &AcZ, &GyX, &GyY, &GyZ);
  accelgyro.resetFIFO();
  AcXCal = AcX - xAccelOff;
  AcYCal = AcY - yAccelOff;
  AcZCal = AcZ - zAccelOff;
  GyXCal = GyX - xGyroOff;
  GyYCal = GyY - yGyroOff;
  GyZCal = GyZ - zGyroOff;
  String data = String(AcXCal) + "," + String(AcYCal) + "," + String(AcZCal) + "," + String(GyXCal) + "," + String(GyYCal) + "," + String(GyZCal) + "_";
  int bufLength = data.length() + 1;
  char dataBuff[bufLength];
  data.toCharArray(dataBuff, bufLength);
  mySerial.write(dataBuff, bufLength);
}

