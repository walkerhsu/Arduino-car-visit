int L3 = 33;
int L2 = 34;
int M = 35;
int R2 = 36;
int R3 = 37;

void setup() {
  pinMode(L3 , INPUT); // 目前預設該接腳作為輸入
  pinMode(L2 , INPUT); // 目前預設該接腳作為輸入
  pinMode(M  , INPUT); // 目前預設該接腳作為輸入
  pinMode(R2 , INPUT); // 目前預設該接腳作為輸入
  pinMode(R3 , INPUT); // 目前預設該接腳作為輸入
  Serial.begin(9600); // 表示開始傳遞與接收序列埠資料
}
void loop(){
int l3 = digitalRead(L3);
int l2 = digitalRead(L2); 
int m  = digitalRead(M);
int r2 = digitalRead(R2);
int r3 = digitalRead(R3);
// 宣告 sensorValue 這變數是整數(Integer)
Serial.print(l2); // 將數值印出來
delay (500); // 延遲 0.5 秒
}
