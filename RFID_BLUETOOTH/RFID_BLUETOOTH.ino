#include <SPI.h>
#include <MFRC522.h>
#include <SoftwareSerial.h>
#define RST_PIN 49
#define SS_PIN 53

MFRC522 *mfrc522;
SoftwareSerial BT (13, 12);
void MotorWriting(double vL , double vR);
void MotorTesting();
void checkHowToGo(char dir);
void Tracking();
void Beep();
void communicate();

int PWMA = 2;
int PWMB = 3;
int AIN1 = 15;
int AIN2 = 14;
int BIN1 = 16;
int BIN2 = 17;
int STBY = 18;

int L3 = 33;
int L2 = 34;
int M = 35;
int R2 = 36;
int R3 = 37;

int turns=0;
int lastError=0;
char c1,c2;
char c[9]={'R','R','B','R','R','B','L','S','L'};
//R:右轉，L:左轉，B:迴轉，S:直走

void setup() {
  pinMode(PWMA, OUTPUT);
  pinMode(STBY, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  
  Serial.begin(9600);
  BT.begin(9600);
  SPI.begin();
  mfrc522 = new MFRC522(SS_PIN, RST_PIN);
  mfrc522->PCD_Init();
  Serial.println(F("Read UID on a MIFARE PICC:"));
}
void loop() { //檢查是否讀取到RFID, 對應的UID 是什麼？
  //Tracking();
  //if(turns==2 || turns==5 || turns==9) Beep();
  Beep();
  communicate();
  //checkHowToGo('N');
}
void MotorWriting(double vL , double vR) {
   digitalWrite(STBY, HIGH);
   if(vL<0) {
      digitalWrite(AIN1,HIGH);
      digitalWrite(AIN2,LOW);
      analogWrite(PWMA , (-1)*vL);
   }
   else if(vL>=0) {
      //向前轉
      digitalWrite(AIN1,LOW);
      digitalWrite(AIN2,HIGH);
      analogWrite(PWMA , vL);
   }
   if(vR<0){
      digitalWrite(BIN1,HIGH);
      digitalWrite(BIN2,LOW);
      analogWrite(PWMB , (-1)*vR);
   }
   else if(vR>=0){
      digitalWrite(BIN1,LOW);
      digitalWrite(BIN2,HIGH);
      analogWrite(PWMB , vR);
   }
}

void Tracking(){
  int l3 = digitalRead(L3);
  int l2 = digitalRead(L2);
  int m  = digitalRead(M);
  int r2 = digitalRead(R2);
  int r3 = digitalRead(R3);
  
  int w3 = 1.5;
  int w2 = 1;
  int Kp = 50;
  int VStraight = 200;
  int Ki = 10;
  
  double vL = 0;
  double vR = 0;
  
  if(l3+l2+m+r2+r3==0) {
    if(turns==9) {
      vL=0;
      vR=0;
    }
    else if(c[turns-1]=='R' || c[turns-1]=='B') {
       vL=100;
       vR=-100;
    }
    else if(c[turns-1]=='L') {
       vL=-100;
       vR=100;
    }
    while((l3+l2+m+r2+r3) == 0) {
      MotorWriting(vL , vR);
      l3 = digitalRead(L3);
      l2 = digitalRead(L2);
      m  = digitalRead(M);
      r2 = digitalRead(R2);
      r3 = digitalRead(R3);
    }
  }
  else if(l3+l2+m+r2+r3==5){
    while((l3+l2+m+r2+r3)==5){
      MotorWriting(VStraight , VStraight);
      l3 = digitalRead(L3);
      l2 = digitalRead(L2);
      m  = digitalRead(M);
      r2 = digitalRead(R2);
      r3 = digitalRead(R3);
    }
    if(turns<=8) checkHowToGo(c[turns]);
    else checkHowToGo('N');
    turns+=1;
  }
  else {
    double error = (l3*(-w3)+l2*(-w2)+r2*(w2)+r3*(w3))/(l3+l2+m+r2+r3);
    double dError = error-lastError;
    double correction = Kp * error + Ki*dError;
    vL = VStraight + correction;
    vR = VStraight - correction;
    if(vL>=255) vL = 255;
    if(vL<=-255) vL = -255;
    if(vR>=255) vR = 255;
    if(vR<=-255) vR = -255;
    lastError = error;
    MotorWriting(vL , vR);
  }
}


void Beep() {
  if(!mfrc522->PICC_IsNewCardPresent()) {
    goto FuncEnd;
  } //PICC_IsNewCardPresent()：是否感應到新的卡片?
  if(!mfrc522->PICC_ReadCardSerial()) {
    goto FuncEnd;
  } //PICC_ReadCardSerial()：是否成功讀取資料?
  Serial.println(F("**Card Detected:**"));
  mfrc522->PICC_DumpDetailsToSerial(&(mfrc522->uid)); //讀出 UID
  mfrc522->PICC_HaltA(); // 讓同一張卡片進入停止模式 (只顯示一次)
  mfrc522->PCD_StopCrypto1(); // 停止 Crypto1

  for ( int i = 0; i < 4; i++ ) { // 卡片UID為4段，分別做比對
    //tmp = mfrc522->uid.uidByte[i]
    BT.print(mfrc522->uid.uidByte[i] , HEX);
  }
  BT.print("\n");
  FuncEnd: ; // goto 跳到這.
}

void communicate() {
  while(Serial.available()) {
    c1=Serial.read();
    BT.write(c1);
  }
  while(BT.available()) {
    c2=BT.read();
    Serial.write(c2);
  }
}

void checkHowToGo(char dir='N'){
  if(dir=='S') {
    //直走
    MotorWriting(100,100);
  }
  else if(dir=='L') {
    //左轉
    MotorWriting(-100,100);
  }
  else if(dir=='R'||dir=='B') {
    //右轉or迴轉
    MotorWriting(100,-100);
  }
  else if(dir=='N'){
    //靜止
    MotorWriting(0,0);
  }
  delay(500);
}
