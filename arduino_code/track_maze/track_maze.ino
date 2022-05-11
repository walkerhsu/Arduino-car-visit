#include <SPI.h>
#include <MFRC522.h>
#include <SoftwareSerial.h>
#define RST_PIN 49
#define SS_PIN 53

MFRC522 *mfrc522;
SoftwareSerial BT (13, 12);

//主程式
void MotorWriting(double vL , double vR); // 給定車車左右輪移動參數
void MotorTesting(); // 藍芽控制馬達
void checkHowToGo(String dir , int curstep); // 從python取得下次前進方向 
void checkIfBeep(String dir , int curstep , int len);
void Tracking();
void Beep();
void BTtoSerial();
void SerialtoBT();

//輔助程式
void MotorTesting(); // 測試馬達

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

//double lastError=0;

char c1,c2;
String dir;
//String dir = "122412442124413333";
// 傳入值為string
int curstep = 0;
int len = 0;
//int len = dir.length();

char c;
//R:右轉，L:左轉，S:直走

bool checkbeep = false;

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
  if (len==0) BTtoSerial();
  else if (len!=0) {
    Tracking();
  }
  if (checkbeep) {
    Beep();
    SerialtoBT();
  }
  
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

  // P control 參數
  double w3 = 3;
  double w2 = 2;
  double Kp = 20;
  double VSL = 210;
  double VSR = 210;
  double Ki = 0;
  
  double vL = 210;
  double vR = 210;

  bool turn = false;
  int checktimes = 0;
  
  // 遇到全白(因為膠帶)
  if(l3+l2+m+r2+r3 == 0) {
    //MotorWriting(vL , vR);
    //delay(1000);
    //MotorWriting(0 , 0);
    //delay(1000);
    if(c == 'R') {
       vL = 100;
       vR = -100;
       //turn = true;
    }
    else if(c == 'L') {
       vL = -100;
       vR = 100;
       //turn = true;
    }
    else if(c == 'S') {
       vL = VSL;
       vR = VSR;
       //turn = false;
    }
//    //繼續執行直到脫離全白
//    while((l3+l2+m+r2+r3) == 0 && turn) {
//      MotorWriting(vL , vR);
//      l3 = digitalRead(L3);
//      l2 = digitalRead(L2);
//      m  = digitalRead(M);
//      r2 = digitalRead(R2);
//      r3 = digitalRead(R3);
//    }
//    while((l3+l2+m+r2+r3) == 0 && (!turn)) {
//      if(checktimes <= 20){
//        vL = -50;
//        vR = 50;
//        checktimes += 1;
//      }
//      else if(checktimes > 20){
//        vL = 50;
//        vR = -50;
//        checktimes += 1;
//      }
//      MotorWriting(vL , vR);
//      l3 = digitalRead(L3);
//      l2 = digitalRead(L2);
//      m  = digitalRead(M);
//      r2 = digitalRead(R2);
//      r3 = digitalRead(R3);
//    }
//    MotorWriting(0 , 0);
//    delay(20);
//    //Serial.print("out of loop")
  }

  else if((l3+l2+m+r2+r3) == 5){
    if(curstep<len) {
      checkHowToGo( dir , curstep);
      checkIfBeep(dir , curstep , len);
      curstep += 1;
    }
    else {
      while(true) MotorWriting(0 , 0);
    }
  }
  //遇到全黑
//  else if((l3+l2+m+r2+r3) == 5){
    //繼續直走至非全黑
//    lastError = 0;
//    MotorWriting(VSL , VSR);
//    delay(200);
//    l3 = digitalRead(L3);
//    l2 = digitalRead(L2);
//    m  = digitalRead(M);
//    r2 = digitalRead(R2);
//    r3 = digitalRead(R3);
//    while((l3+l2+m+r2+r3) == 5){
//      if(l3 == 0){
//        MotorWriting(150 , -150);
//        delay(50);
//      }
//      else if(r3 == 0){
//        MotorWriting(-150 , 150);
//        delay(50);
//      }
//      else {
//        MotorWriting(VSL , VSR);
//      }
//      MotorWriting(VSL , VSR);
//
//      l3 = digitalRead(L3);
//      l2 = digitalRead(L2);
//      m  = digitalRead(M);
//      r2 = digitalRead(R2);
//      r3 = digitalRead(R3);
//      
//    }
//    MotorWriting(0 , 0);
//    delay(1000);
//    if(curstep<len) {
//      checkHowToGo( dir , curstep);
//      checkIfBeep(dir , curstep , len);
//      curstep += 1;
//    }
//    else {
//      while (true) MotorWriting(0,0);
//    } 
//    if(c == 'R') {
//       vL = 150;
//       vR = -150;
//       turn = true;
//    }
//    else if(c == 'L') {
//       vL = -150;
//       vR = 150;
//       turn = true;
//    }
//    else if(c == 'S') {
//       vL = VSL;
//       vR = VSR;
//       turn = false;
//    }
//    l3 = digitalRead(L3);
//    l2 = digitalRead(L2);
//    m  = digitalRead(M);
//    r2 = digitalRead(R2);
//    r3 = digitalRead(R3);
//    //繼續執行直到脫離全白
//    while((l3+l2+m+r2+r3) == 0 && turn) {
//      MotorWriting(vL , vR);
//      l3 = digitalRead(L3);
//      l2 = digitalRead(L2);
//      m  = digitalRead(M);
//      r2 = digitalRead(R2);
//      r3 = digitalRead(R3);
//    }
//    while((l3+l2+m+r2+r3) == 0 && (!turn)) {
//      MotorWriting(0, 0);
//      delay(1000);
//      if(checktimes <= 20){
//        vL = -50;
//        vR = 50;
//        checktimes = checktimes + 1;
//      }
//      else if(checktimes > 20){
//        vL = 50;
//        vR = -50;
//        checktimes = checktimes + 1;
//      }
//      MotorWriting(vL , vR);
//      l3 = digitalRead(L3);
//      l2 = digitalRead(L2);
//      m  = digitalRead(M);
//      r2 = digitalRead(R2);
//      r3 = digitalRead(R3);
//    }
//    MotorWriting(0 , 0);
//    delay(300);
//    MotorWriting(0 , 0);
//    delay(500);
  //}

  // PD control
  else {
    double error = (l3*((-1)*w3)+l2*((-1)*w2)+r2*(w2)+r3*(w3))/(l3+l2+m+r2+r3);
    //double dError = error - lastError;
    double correction = Kp * error;// + Ki*dError;
//    if(error<0) {
//      MotorWriting(0 , 0);
//      delay(100);
//    }
    vL = VSL + correction ;
    vR = VSR - correction ;
    if(vL>=250) {
      vR = vR -  (vL-250);
      vL = 250;
    }
    else if(vL<=-250) vL = -250;
    
    if(vR>=250) {
      vL = vL -  (vR-250);
      vR = 250;
    }
    else if(vR<=-250) vR = -250;
    
    //lastError = error;
    MotorWriting(vL , vR);
    
  }

//  // P control
//  else {
//    double error = (l3*(-w3)+l2*(-w2)+r2*(w2)+r3*(w3))/(l3+l2+m+r2+r3);
//    double correction = Kp * error;
//    vL = VStraight + correction;
//    vR = VStraight - correction;
//    if(vL>=255) vL = 255;
//    if(vL<=-255) vL = -255;
//    if(vR>=255) vR = 255;
//    if(vR<=-255) vR = -255;
//    MotorWriting(vL , vR);
//  }


  
}


void Beep() {
  if(!mfrc522->PICC_IsNewCardPresent()) {
    goto FuncEnd;
  } //PICC_IsNewCardPresent()：是否感應到新的卡片?
  if(!mfrc522->PICC_ReadCardSerial()) {
    goto FuncEnd;
  } //PICC_ReadCardSerial()：是否成功讀取資料?
  //Serial.println(F("*Card Detected:*"));
  mfrc522->PICC_DumpDetailsToSerial(&(mfrc522->uid)); //讀出 UID
  mfrc522->PICC_HaltA(); // 讓同一張卡片進入停止模式 (只顯示一次)
  mfrc522->PCD_StopCrypto1(); // 停止 Crypto1

  for ( int i = 0; i < 4; i++ ) { // 卡片UID為4段，分別做比對
    int tmp = mfrc522->uid.uidByte[i];
    if(tmp<=15) {
      BT.print(0 , HEX);
    }
    BT.print(tmp , HEX);
  }
  BT.print("\n");
  FuncEnd: ; // goto 跳到這.
}

void BTtoSerial() {
  while(BT.available()) {
    c2=BT.read();
    dir=dir+c2;
    Serial.write(c2);
  }
  //Serial.write(len);
  len = dir.length();
}

void SerialtoBT() {
  while(Serial.available()) {
    c1=Serial.read();
    BT.write(c1);
  }
}

//void checkHowToGo(String dir , int curstep){
//  int VSL = 210;
//  int VSR = 210;
//  int dtime = 370;
//  if(curstep==0) {
//    // 直走
//    c = 'S';
//    MotorWriting( VSL , VSR );
//    dtime = 10;
//  }
//  else {
//    int movement = dir[curstep] - dir[curstep-1];
//    if((movement == 0)){
//      // 直走
//      c = 'S';
//      MotorWriting( VSL , VSR );
//      dtime = 10;
//    }
//    else if((movement == -1) || (movement == 3)) {
//      //左轉
//      MotorWriting( VSL , VSR );
//      delay(50);
//      c = 'L';
//      MotorWriting(-150,150);
//    }
//    else if((movement == 1) || (movement == -3)) {
//      //右轉
//      MotorWriting( VSL , VSR );
//      delay(50);
//      c = 'R';
//      MotorWriting(150,-150);
//    }
//    else if((movement == 2) || (movement == -2)) {
//      //迴轉
//      MotorWriting( VSL , VSR );
//      delay(50);
//      c = 'R';
//      MotorWriting(150,-150);
//      dtime = 750;
//    }
//    else{
//      //靜止
//      c = 'N';
//      MotorWriting(0,0);
//    }
//  }
//  delay( dtime );
////  MotorWriting(0,0);
////  delay(1000);
//}

void checkIfBeep(String dir , int curstep , int len) {
  if(curstep==0 ) checkbeep = true;
  else if(curstep==(len-1)) checkbeep = true;
  else if(dir[curstep+1]-dir[curstep]==2 || dir[curstep+1]-dir[curstep]==-2) checkbeep = true;
  else checkbeep = false;
}

void checkHowToGo(String dir , int curstep){
  int VSL = 210;
  int VSR = 210;
  int l3 = digitalRead(L3);
  int l2 = digitalRead(L2);
  int m  = digitalRead(M);
  int r2 = digitalRead(R2);
  int r3 = digitalRead(R3);
  if(curstep==0) {
    // 直走
    while(l3+l2+m+r2+r3==4 || l3+l2+m+r2+r3==5) {
        MotorWriting( VSL , VSR );
        l3 = digitalRead(L3);
        l2 = digitalRead(L2);
        m  = digitalRead(M);
        r2 = digitalRead(R2);
        r3 = digitalRead(R3);
      }
      c = 'S';
  }
  else {
    int movement = dir[curstep] - dir[curstep-1];
    if((movement == 0)){
      // 直走
      while(l3+l2+m+r2+r3==4 || l3+l2+m+r2+r3==5) {
        MotorWriting( VSL , VSR );
        l3 = digitalRead(L3);
        l2 = digitalRead(L2);
        m  = digitalRead(M);
        r2 = digitalRead(R2);
        r3 = digitalRead(R3);
      }
      c = 'S';
    }
    else if((movement == -1) || (movement == 3)) {
      //左轉
      while(!(r3==0 && (l2==1 || m==1))) {
        MotorWriting( 105 , 255 );
        l3 = digitalRead(L3);
        l2 = digitalRead(L2);
        m  = digitalRead(M);
        r2 = digitalRead(R2);
        r3 = digitalRead(R3);
      }
      MotorWriting( 0 , 0 );
      delay(20);
      //delay(720);
      c = 'L';
    }
    else if((movement == 1) || (movement == -3)) {
      //右轉
      while(!(l3==0 && (r2==1 || m==1))){
        MotorWriting( 255 , 105 );
        l3 = digitalRead(L3);
        l2 = digitalRead(L2);
        m  = digitalRead(M);
        r2 = digitalRead(R2);
        r3 = digitalRead(R3);
      }
      MotorWriting( 0 , 0 );
      delay(20);
      //delay(650);
      c = 'R';
      
    }
    else if((movement == 2) || (movement == -2)) {
      //迴轉
      MotorWriting( 0 , 0 );
      delay(160);
      MotorWriting( 255 ,-255 );
      delay(455);
      c = 'R';
      MotorWriting( 0 , 0 );
      delay(160);
    }
    else{
      //靜止
      c = 'N';
      MotorWriting(0,0);
    }
  }
//  MotorWriting(0,0);
//  delay(1000);
}
