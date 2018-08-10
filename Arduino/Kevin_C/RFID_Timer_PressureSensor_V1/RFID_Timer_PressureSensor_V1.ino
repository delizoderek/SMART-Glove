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

//Global variables for pressure sensor
int PressurePin1 = A2;
int PressurePin2 = A1;
int index;
int middle;
int LEDpin1 = 3;
int LEDpin2 = 4;
char level = '1'; //This indicates the pressure level
int data;        

void setup() {
  // put your setup code here, to run once:
  //Relates to Index finger
  pinMode(LEDpin1,OUTPUT);
  pinMode(PressurePin1,INPUT);
  
  //Relates to Middle Finger
  pinMode(LEDpin2,OUTPUT);
  pinMode(PressurePin2,INPUT);
  Serial.begin(9600);
  //Setup for timer

  //Setup for RFID
  SPI.begin(); //Init SPI bus
  rfid.PCD_Init(); // Init MFRC522

  for(byte i = 0; i <6; i++) {
    key.keyByte[i] = 0xFF;
  }
  
}


void loop() {    
   if(level == '1'){
    data = 200;
   }
   else if(level == '2') {
    data = 400; 
   }
   else if(level == '3') {
    data = 600;
   }else{
    Serial.println("Invalid");
   }
   index = analogRead(PressurePin1);
   middle = analogRead(PressurePin2);
   if(index > data) {
    digitalWrite(LEDpin1,HIGH);
   // Serial.println("Index Pressed");
   }else{
    digitalWrite(LEDpin1,LOW);
   // Serial.println("Index Released");
   }
   if(middle > data){
    digitalWrite(LEDpin2,HIGH);
   // Serial.println("Middle Pressed");
   }else{
    digitalWrite(LEDpin2,LOW);
   // Serial.println("Middle Released");
   }
   delay(10);
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
    if(strID.indexOf("8A:37:B5:63") >= 0) { //For blue tag
    //if(strID.indexOf("93:B5:34:24") >= 0) { //For white card
   if(test == false){ //False means it is on
    Serial.println("It is on");
    //Add an action while the system is on
    startTime = millis();
    //Serial.print("Start Time: ");  //Will show start serial time
    
    //Serial.println(startTime);    //Will print out start serial time
   }else{
    
    Serial.println("It is off");
    //Add an actions while the system turns off
    StopTime(); //Function
   }
   test = !test;
   
  }
 
  // Halt PICC
   rfid.PICC_HaltA();

  // Stop encryption on PCD
   rfid.PCD_StopCrypto1();

}

//Stop time function: Called to initiation actions after timer is called
//Will calculate the time elapsed between RFID scans in seconds.
//V2 will convert time in seconds to minutes, and hours  
void StopTime(){
  stopTime = millis();
  Serial.print("Time elapsed: ");
   unsigned long timeElapsed = stopTime - startTime; //This varaible createds the total time elapsed
    
   Serial.println((float)(timeElapsed/1000.0));  //Will print out time elapsedin seconds
    float sec = timeElapsed/1000.0;
    
    int min  = (int) (sec/60); //This will divide up the seconds and convert into minutes
    int hour = (min/60);      //This would convert the minutes into hours 

    while(sec > 60.0){  //This will reduce the value of seconds to be displayed beterrn
      sec = sec - 60.0; //0.00 and 59.99 seconds. It will be ran while the second value is above
    }                   //60.00

    //This will print out the time on the serial. The actual value that will be taken
    //Sec
    Serial.println("Time");
    Serial.print(hour);   //Time represented in Hours
    Serial.print(" h: ");
    Serial.print(min);    //Time represented in Minutes
    Serial.print(" m: ");
    Serial.print(sec);    //Time represented in Seconds
    Serial.print(" s");
}

//This is the action for the pressure sensor simple as that
void Pressuresensorpress(){
  
}

