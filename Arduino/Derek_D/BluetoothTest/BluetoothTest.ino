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
float AcXCal, AcYCal, AcZCal, GyXCal, GyYCal, GyZCal;
float samples;
int baudrate = 9600;
int i = 0;
bool isLinked;
bool isCalibrating;
bool isTransmitting;
bool xCal;
int atOrigin;
int pressStrength;
int countdown;
int buttonState = 0;
int fingerTap = 0;
SoftwareSerial mySerial(2, 3);

void setup()
{
  Serial.begin(baudrate);
  mySerial.begin(baudrate);
  Serial.println("Intializing IMU");
  InitIMU();
  //accelgyro.initialize();
  Serial.println("Testing Connections");
  //Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
  isTransmitting = false;
  isCalibrating = false;
  samples = 400;
  countdown = 5;
  atOrigin = 0;
  xCal = false;
  pinMode(7, INPUT_PULLUP);
}

void InitIMU(){
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
}

void loop()
{
  //buttonState = digitalRead(7);
//  if(!(buttonState == LOW)){
//    atOrigin = 1;
//  }
  if (isTransmitting) {
    Serial.println("Transmitting");
    if (countdown <= 0) {
      digitalWrite(6, HIGH);
      AcXCal /= 5;
      AcYCal /= 5;
      AcZCal /= 5;
      GyXCal /= 5;
      GyYCal /= 5;
      GyZCal /= 5;
      SendData(AcXCal, AcYCal, AcZCal, GyXCal, GyYCal, GyZCal);
      AcXCal = 0;
      AcYCal = 0;
      AcZCal = 0;
      GyXCal = 0;
      GyYCal = 0;
      GyZCal = 0;
      atOrigin = 0;
      fingerTap = 0;
      countdown = 5;
    } else {
      ReadData();
      //accelgyro.getMotion6(&AcX, &AcY, &AcZ, &GyX, &GyY, &GyZ);
      //accelgyro.resetFIFO();
      AcXCal += AcX;
      AcYCal += AcY;
      AcZCal += AcZ;
      GyXCal += GyX;
      GyYCal += GyY;
      GyZCal += GyZ;
      countdown--;
    }
  }
  
  if (isCalibrating) {
    Serial.println("Made it Here");
    if (samples <= 0) {
      Serial.println("Calibration Complete");
      mySerial.write('d');
      //isTransmitting = true;
      isCalibrating = false;
      digitalWrite(6, HIGH);
    } else if (samples <= 500) {
      Serial.println("Calibration Step   Samples: " + String(samples));
      //accelgyro.getMotion6(&AcX, &AcY, &AcZ, &GyX, &GyY, &GyZ);
      //accelgyro.resetFIFO();
      ReadData();
      SendData(AcX, AcY, AcZ, GyX, GyY, GyZ);
      samples--;
    } else {
      samples--;
      Serial.println(samples);
      //mySerial.write('c');
    }
  }

  if (mySerial.available()) {
    Serial.println("GO");
    char in = mySerial.read();
    switch (in) {
      case 'c':
        Serial.println("Preparing Data");
        isCalibrating = true;
        samples = 400;
        isTransmitting = false;
        break;
      case 't':
        Serial.println("Transmitting Data");
        isTransmitting = true;
        isCalibrating = false;
        break;
      case 'd':
        Serial.println("Done");
        isTransmitting = false;
        isCalibrating = false;
        break;
    }
  }

  delay(50);
}

void ReadData(){
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr,14,true);  // request a total of 14 registers
  AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)     
  AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  Tmp=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  GyX=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  GyY=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  GyZ=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
}

void SendData(float Ax, float Ay, float Az, float Gx, float Gy, float Gz) {
  String data = String(Ax) + "," + String(Ay) + "," + String(Az) + "," + String(Gx) + "," + String(Gy) + "," + String(Gz) + "," + String(atOrigin) + "," + String(fingerTap) + "_";
  int bufLength = data.length() + 1;
  char dataBuff[bufLength];
  data.toCharArray(dataBuff, bufLength);
  mySerial.write(dataBuff, bufLength);
}

