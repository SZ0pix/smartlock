#include "FPS_GT511C3.h"
#include <SoftwareSerial.h>


#define SerialRX 4   
#define SerialTX 5

int message[]={0,0}; //info from scanner to RPi

FPS_GT511C3 fps(SerialRX, SerialTX); // add scanner

void openLock()                      //sends signal to relay  
  {
  digitalWrite(8, HIGH);
 // digitalWrite(G, LOW);
  delay(1000);
  //digitalWrite(signalPin, HIGH);
  digitalWrite(8, LOW);
  }









void setup() {
  Serial.begin(9600); //set up Arduino's hardware serial UART
  //fps.UseSerialDebug = true; // so you can see the messages in the serial debug screen
  fps.Open(); //send serial command to initialize fps
  fps.SetLED(true);
  pinMode(11,OUTPUT);
  pinMode(13,OUTPUT);
  pinMode(8,OUTPUT);
}

void checkScanner(){
    digitalWrite(11,LOW);     //led for diagnostisc 
    digitalWrite(13,HIGH);    //to be erased in future
    fps.CaptureFinger(false);
    int id = fps.Identify1_N();
    if (id <200) //for GT-521F32 only 200 fingerprints available
    {//if the fingerprint matches send arrey [1][id] by serial to arduino
      message[0]=1;
      message[1]=id;
      Serial.print(message[0]);
      Serial.print(message[1]);
      Serial.print("\n");
      openLock();  //unlock doors
    }
    else
    {//if unable to recognize send arrey [0][999] by serial
      message[0]=0;
      message[1]=999;
      Serial.print(message[0]);
      Serial.print(message[1]);
      Serial.print("\n");
    }
  }








void loop() {
  if (fps.IsPressFinger()){
   checkScanner();}
  else{
   //nothing happens;
   digitalWrite(11,HIGH); //led for diagnosics
   digitalWrite(13,LOW);
  }  
 
  delay(200);
}
