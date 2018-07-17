/*Kevin Chung
 * Created on 7/16/2018
 * SMART Glove RFID scanner + timer
 * Decription: The script will measure the time elapsed between RFID scans.
 * 
 */
#include <SPI.h> 
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 rfid(SS_PIN, RST_PIN); //INstance of the class

MFRC522::MIFARE_Key key;

//Init array that will stroe new NUID
byte nuidPICC[4];
bool test = false; //Global Variable
unsigned long startTime = 0;
unsigned long stopTime = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //Setup for timer

  //Setup for RFID
  SPI.begin(); //Init SPI bus
  rfid.PCD_Init(); // Init MFRC522

  for(byte i = 0; i <6; i++) {
    key.keyByte[i] = 0xFF;
  }

//For testing purposes. Comment out for skelepton output
//Can prompt to begin action or something
  //Serial.print(F("Begin timer"));
 // printHex(key.keyByte, MFRC522::MF_KEY_SIZE);
  
}


void loop() {    
  // put your main code here, to run repeatedly:
     if ( ! rfid.PICC_IsNewCardPresent())
    return;

    // Verify if the NUID has been readed
  if ( ! rfid.PICC_ReadCardSerial())
    return;

   
  //This code, once rfid is scanned, will collect the tag ID in Hex
  //And will store it as a String called strID
    String strID = "";
    for(byte i = 0; i < 4; i++) {
      strID +=
        (rfid.uid.uidByte[i] < 0x10 ? "0" : "") + 
        String(rfid.uid.uidByte[i],HEX) + 
        (i != 3 ? ":" : "");
  }
  
  //The string will be formatted and all letters will be uppercased
  strID.toUpperCase();
  Serial.print("Key Card ID (HEX)");
  Serial.println(strID);

 //Once we have the ID, we can create an if statement to activate something
  if(strID.indexOf("8A:37:B5:63") >= 0) {
    
   if(test == false){ //False means it is on
    Serial.println("It is on");
    //Add an action while the system is on
    startTime = millis();
    //Serial.print("Start Time: ");  //Will show start serial time
    
    //Serial.println(startTime);    //Will print out start serial time
   }else{
    
    Serial.println("It is off");
    //Add an action while the system turns off
    stopTime = millis();
    Serial.print("Time elapsed: " );
    unsigned long timeElapsed = stopTime - startTime;
    Serial.println((float)(timeElapsed/1000.0));  //Will print out time elapsedin seconds
    
    //Serial.println(time);
   }
   test = !test;
   
  }
 
  

  // Halt PICC
  rfid.PICC_HaltA();

    // Stop encryption on PCD
  rfid.PCD_StopCrypto1();
}


/**
 * Helper routine to dump a byte array as hex values to Serial. 
 */
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

/**
 * Helper routine to dump a byte array as dec values to Serial.
 */
void printDec(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], DEC);
  }
}


