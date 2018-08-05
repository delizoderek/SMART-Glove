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
bool isCalibrated;
SoftwareSerial mySerial(2, 3);

void setup()
{
  Serial.begin(baudrate);
  mySerial.begin(baudrate);
  Serial.println("Intializing IMU");
  accelgyro.initialize();
  Serial.println("Testing Connections");
  Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
  isLinked = false;
  isCalibrated = false;
  samples = 1100;
}

void loop()
{
  if (isLinked & isCalibrated) {
    SendData();
  }

  if (isCalibrated == false) {
    if (samples <= 0) {
      xAccelOff /= 1000;
      yAccelOff /= 1000;
      zAccelOff /= 1000;
      xGyroOff /= 1000;
      yGyroOff /= 1000;
      zGyroOff /= 1000;
      isCalibrated = true;
      Serial.println("Calibration Complete");
      Serial.print("AX Offset: " + String(AcX));
      Serial.print(" AY Offset: " + String(AcY));
      Serial.print(" AZ Offset: " + String(AcZ));
      Serial.print(" GX Offset: " + String(GyX));
      Serial.print(" GY Offset: " + String(GyY));
      Serial.println(" GZ Offset: " + String(GyZ) + "\n \n");
    } else  if (samples < 1000) {
      Serial.println("Collecting Samples");
      Serial.println("Samples Collected so far: " + String(1000 - samples));
      accelgyro.getMotion6(&AcX, &AcY, &AcZ, &GyX, &GyY, &GyZ);
      xAccelOff += AcX;
      yAccelOff += AcY;
      zAccelOff += AcZ;
      xGyroOff += GyX;
      yGyroOff += GyY;
      zGyroOff += GyZ;
      samples--;
    } else {
      samples--;
    }
  }

  if (mySerial.available()) {
    Serial.println("Connected");
    isLinked = true;
  }

  delay(10);
}

void SendData() {
  float AcXCal, AcYCal, AcZCal, GyXCal, GyYCal, GyZCal;
  AcXCal = (AcX - xAccelOff) / 16384.0;
  AcYCal = (AcY - yAccelOff) / 16384.0;
  AcZCal = (AcZ - zAccelOff) / 16384.0;
  GyXCal = (GyX - xGyroOff) / 131.0;
  GyYCal = (GyY - yGyroOff) / 131.0;
  GyZCal = (GyZ - zGyroOff) / 131.0;
  String data = String(AcXCal) + "," + String(AcYCal) + "," + String(AcZCal) + "," + String(GyXCal) + "," + String(GyYCal) + "," + String(GyZCal) + "_";
  int bufLength = data.length() + 1;
  char dataBuff[bufLength];
  data.toCharArray(dataBuff, bufLength);
  mySerial.write(dataBuff, bufLength);
}

