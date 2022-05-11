int PWMA = 2;
int PWMB = 3;
int AIN1 = 15;
int AIN2 = 14;
int BIN1 = 16;
int BIN2 = 17;
int STBY = 18;
void setup() {
  pinMode(PWMA, OUTPUT);
  pinMode(STBY, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  
  Serial.begin(9600);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  MotorWriting(100 , 250);
  delay(640);
  MotorWriting(0 , 0);
  delay(10000);
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
