/*
 * Capstone II Project
 * This program gathers input data from a pressure sensor to track
 * it's position, speed, and time
 * 
 * MPU6050 Datasheet: https://www.invensense.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf
 */
#include <Wire.h>

const int PinButton = 3;
const int LED = 4;

long aX, aY, aZ;
float fX, fY, fZ;

long gX, gY, gZ;
float rotX, rotY, rotZ;

void setup() {
  pinMode(PinButton, INPUT);
  digitalWrite(PinButton, HIGH);
  pinMode(LED, OUTPUT);
  
  Serial.begin(9600);
  Wire.begin();
  setupIMU();
 
}

void loop() {
  if (digitalRead(PinButton) == LOW) {
    digitalWrite(LED, HIGH);
    
    resetToOrigin();
    printData();
    delay(500);
    
  } else {
    digitalWrite(LED, LOW); 
    recordAccelData();
    recordGyroData();
    printData();
    delay(500);
  }
  
 
}

void resetToOrigin() {
  Wire.beginTransmission(0b1101000);
  Wire.write(0x3B);
  Wire.endTransmission();
  Wire.requestFrom(0b1101000, 6);

  while(Wire.available() < 6);
  aX = Wire.read() << 0b0000000;
  aY = Wire.read() << 0b0000000;
  aZ = Wire.read() << 0b0000000;

  processAccelData();
}

void setupIMU() {
  Wire.beginTransmission(0b1101000); //7-bit address of I2C MPU change LSB 0/1 - low/high
  Wire.write(0x6B); //register 6B
  Wire.write(0b0000000); //sleep register set to 0
  Wire.endTransmission();

  Wire.beginTransmission(0b1101000); //access address of IMU
  Wire.write(0x1B); //accessing gyroscope register
  Wire.write(0xb0000000); //setting range of gyro o/p to +/- 250d/s
  Wire.endTransmission();

  Wire.beginTransmission(0b1101000);
  Wire.write(0x1C); //registering accelerometer
  Wire.write(0xb0000000); //setting range of accelerometer to +/- 2g
  Wire.endTransmission();
}

void recordAccelData() {
  Wire.beginTransmission(0b1101000);
  Wire.write(0x3B);
  Wire.endTransmission();
  Wire.requestFrom(0b1101000, 6); //request data from the acclerometer x,y,z
  
  while(Wire.available() < 6);
  aX = Wire.read() << 8|Wire.read();
  aY = Wire.read() << 8|Wire.read();
  aZ = Wire.read() << 8|Wire.read();
  processAccelData();
}

void processAccelData() {
  //16384 represents the sensitivity of the accelerometer to +/- 2g
  fX = aX / 16384.0;
  fY = aY / 16384.0;
  fZ = aZ / 16384.0;
}

void recordGyroData() {
  Wire.beginTransmission(0b1101000);
  Wire.write(0x43);
  Wire.endTransmission();
  Wire.requestFrom(0b1101000, 6);

  while(Wire.available() < 6);
  gX = Wire.read() << 8|Wire.read();
  gY = Wire.read() << 8|Wire.read();
  gZ = Wire.read() << 8|Wire.read();
  processGyroData();
}

void processGyroData() {
//uncomment to adjust sensitivity
  
  //sensitivity +/- 250 dg/s
  rotX = gX / 131.0;
  rotY = gY / 131.0;
  rotZ = gZ / 131.0;

  //sensitivity +/- 500 dg/s
  /*
  rotX = gX / 65.5;
  rotY = gY / 65.5;
  rotZ = gZ / 65.5;
  */
  
  //sensitivity +/- 1000 dg/s
  /*
  rotX = gX / 32.8;
  rotY = gY / 32.8;
  rotZ = gZ / 32.8;
  */
  
  //sensitivity +/- 2000 dg/s
  /*
  rotX = gX / 16.4;
  rotY = gY / 16.4;
  rotZ = gZ / 16.4;
  */
}

void printData() {
  Serial.print("Gyro (Deg)");
  Serial.print(" X= ");
  Serial.print(rotX);

  Serial.print(" Y= ");
  Serial.print(rotY);

  Serial.print(" Z= ");
  Serial.print(rotZ);

  Serial.print(" Accel (g)");
  Serial.print(" X= ");
  Serial.print(fX);

  Serial.print(" Y= ");
  Serial.print(fY);

  Serial.print(" Z= ");
  Serial.print(fZ);
  Serial.println();
}

