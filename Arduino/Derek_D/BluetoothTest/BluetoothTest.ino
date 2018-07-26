/*
 * Created by Derek DeLizo
 * TX -> D2
 * RX -> D3
*/
#include <SoftwareSerial.h>
int baudrate = 9600;
int i = 0;
SoftwareSerial mySerial(2,3);

int data[17][6] = {{0,0,0,0,0,0},
                {0,0,0,0,0,1},
                {0,0,0,0,1,0},
                {0,0,0,0,1,1},
                {0,0,0,1,0,0},
                {0,0,0,1,0,1},
                {0,0,0,1,1,0},
                {0,0,0,1,1,1},
                {0,0,1,0,0,0},
                {0,0,1,0,0,1},
                {0,0,1,0,1,0},
                {0,0,1,0,1,1},
                {0,0,1,1,0,0},
                {0,0,1,1,0,1},
                {0,0,1,1,1,0},
                {0,0,1,1,1,1},
                {0,1,0,0,0,0}
               };
void setup() 
{
    Serial.begin(baudrate);
    while(!Serial){
      ;  
    }
    mySerial.begin(baudrate);
}
 
void loop()
{
  if(mySerial.available()){
    int buf[6] = getData();
    mySerial.write(buf,6);
  }
}

public int[] getData(){
  int datum[6];
  for(int m = 0; m < 6; m++){
    datum[m] = data[i][m];
  }
  return datum;
}
