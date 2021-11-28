#include "FPS_GT511C3.h"
#include "SoftwareSerial.h"

#define D 14
#define B 15
#define SerialRX 10   
#define SerialTX 11

FPS_GT511C3 fps(SerialRX, SerialTX); // add scanner
int tab[3];
int relay_time;


void open_lock(int value){
   relay_time=value;
   digitalWrite(D,HIGH);
   relay_time=relay_time*1000;
   delay(relay_time);
   digitalWrite(D,LOW);
  }

 
void enroll() {
  digitalWrite(D,HIGH);
  delay(50);
  digitalWrite(D,LOW);
  delay(50);
  digitalWrite(D,HIGH);
  delay(50);
  digitalWrite(D,LOW);
  delay(50);
  digitalWrite(D,HIGH);
  delay(50);
  digitalWrite(D,LOW);
  delay(50);
  digitalWrite(D,HIGH);
  delay(50);
  digitalWrite(D,LOW);
  
  
  }

  

void setup() {
  Serial.begin(9600);
  Serial2.begin(9600);
  pinMode(D,OUTPUT);
  pinMode(B,INPUT_PULLUP);
  digitalWrite(D,LOW);
  fps.Open();
  fps.SetLED(true);
  tab[0]=1;
  tab[1]=2;
  tab[2]=3;
  
}

void loop() {
  if(digitalRead(B)==LOW){
    Serial.print('<');
    Serial.print(tab[0]);
    Serial.print(';');
    Serial.print(tab[1]);
    Serial.print(';');
    Serial.print(tab[2]);
    Serial.print('>');
    delay(200);
    }
  else{;}
    
  if (Serial.available() > 0) {
    String odczyt = Serial.readStringUntil('\n');
    if (odczyt[1]=='1' && odczyt[3]=='0'){
      int value = String(odczyt[5]).toInt();
      open_lock(value);}     
      else if (odczyt[1]=='9' && odczyt[3]=='9' && odczyt[5]=='0'){
      enroll();}
      else{;}}



   if(fps.IsPressFinger())
    {
    Serial.println("...");
    fps.CaptureFinger(false);
    int id = fps.Identify1_N(); 
    if(id<200){
    tab[0]=1;
    tab[1]=0;
    tab[2]=id;}
    else{
    tab[0]=0;
    tab[1]=0;
    tab[2]=9;}
    delay(20);
    }
 
}
