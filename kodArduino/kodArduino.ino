#include "FPS_GT511C3.h"
#include "SoftwareSerial.h"

#define D 13        //diode for testing, relay in final version
#define SerialRX 10   
#define SerialTX 11

FPS_GT511C3 fps(SerialRX, SerialTX); // add scanner
int tab[3];
int relay_time_arduino=4000;
int relay_time;

void open_lock(int value){
   relay_time=value;
   digitalWrite(D,LOW);
   relay_time=relay_time*1000;
   relay_time_arduino=relay_time;
   delay(relay_time);
   digitalWrite(D,HIGH);
  }

  void open_lock2(int value){
   digitalWrite(D,LOW);
   delay(value);
   digitalWrite(D,HIGH);
  }

void print_frame(int a, int b, int c){
    Serial.print('<');
    Serial.print(a);
    Serial.print(';');
    Serial.print(b);
    Serial.print(';');
    Serial.print(c);
    Serial.print('>');
}

 
void enroll() {
  int enrollid = 0;                               // find open enroll id
  bool usedid = true;
  while (usedid == true){
    usedid = fps.CheckEnrolled(enrollid);
    if (usedid==true) enrollid++;
  }
    
  fps.EnrollStart(enrollid);
  
  // enroll  
  print_frame(9,1,0);                             //"Press finger to Enroll #"
  while(fps.IsPressFinger() == false) delay(100);
  bool bret = fps.CaptureFinger(true);
  int iret = 0;
  if (bret != false)  
  {
    print_frame(9,3,0);                           //"Remove finger"
    fps.Enroll1(); 
    while(fps.IsPressFinger() == true) delay(100);
    print_frame(9,2,0);                           //"Press same finger again"
    while(fps.IsPressFinger() == false) delay(100);
    bret = fps.CaptureFinger(true);
    if (bret != false)
    {
      print_frame(9,3,0);                         //"Remove finger"
      fps.Enroll2();
      while(fps.IsPressFinger() == true) delay(100);
      print_frame(9,2,0);                         //"Press same finger yet again"
      while(fps.IsPressFinger() == false) delay(100);
      bret = fps.CaptureFinger(true);
      if (bret != false)
      {
        print_frame(9,3,0);                       //"Remove finger"
        iret = fps.Enroll3();
        delay(1000);
        if (iret == 0){
          delay(500);
          print_frame(9,4,enrollid);              //"Enrolling Successful"   + enrollid
        }
        else{
          print_frame(9,8,iret);                  //"Enrolling Failed with error code:"
        }
      }
      else print_frame(9,7,0);                    //"Failed to capture third finger"
    }
    else print_frame(9,6,0);                      //"Failed to capture second finger"
  }
  else print_frame(9,5,0);                        //"Failed to capture first finger"
  }

  

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(300);
  //Serial2.begin(9600);
  pinMode(D,OUTPUT);
  digitalWrite(D,HIGH);
  fps.Open();
  fps.SetLED(true);
  tab[0]=1;
  tab[1]=2;
  tab[2]=3;
  
}

void loop() {

//reading data recived from RaspberryPI    
  if(Serial.available() > 0) {
    String odczyt = Serial.readStringUntil('\n');
              //request to open lock
    if (odczyt[1]=='1' && odczyt[3]=='0'){    
      int value = String(odczyt[5]).toInt();
      open_lock(value);}    
              //request to start enroll 
    else if (odczyt[1]=='9' && odczyt[3]=='9' && odczyt[5]=='0'){
      enroll();
      delay(2000);}
    else{;}}

// scanning finger
   if(fps.IsPressFinger()){
      fps.CaptureFinger(false);
      int id = fps.Identify1_N(); 
      if(id<200){
        print_frame(1,0,id);
        open_lock2(relay_time_arduino);}
      else{
      print_frame(0,0,9);
      delay(20);
      }}
 
}
