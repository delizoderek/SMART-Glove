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
bool originaTap;
int pressStrength;
int countdown;
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
  samples = 400;
  countdown = 5;
  xCal = false;
  pinMode(6, OUTPUT);
}

void loop()
{
  if (isTransmitting) {
    Serial.println("Should not be Here");
    if (countdown <= 0) {
      digitalWrite(6, LOW);
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
      countdown = 5;
    } else {
      accelgyro.getMotion6(&AcX, &AcY, &AcZ, &GyX, &GyY, &GyZ);
      accelgyro.resetFIFO();
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
      accelgyro.getMotion6(&AcX, &AcY, &AcZ, &GyX, &GyY, &GyZ);
      accelgyro.resetFIFO();
      SendData(AcX, AcY, AcZ, GyX, GyY, GyZ);
      samples--;
    } else {
      samples--;
      Serial.println(samples);
      //mySerial.write('c');
    }
  }

  if (mySerial.available()) {
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
      default:
        isTransmitting = false;
        isCalibrating = false;
        break;
    }
  }

  delay(50);
}

void SendData(float Ax, float Ay, float Az, float Gx, float Gy, float Gz) {
  String data = String(Ax) + "," + String(Ay) + "," + String(Az) + "," + String(Gx) + "," + String(Gy) + "," + String(Gz) + "_";
  int bufLength = data.length() + 1;
  char dataBuff[bufLength];
  data.toCharArray(dataBuff, bufLength);
  mySerial.write(dataBuff, bufLength);
}

