/***************************************************************************/
// File			  [track.h]
// Author		  [Erik Kuo]
// Synopsis		[Code used for tracking]
// Functions  [MotorWriting, MotorInverter, tracking]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

#include <SoftwareSerial.h>
#include <Wire.h>

/*if you have no idea how to start*/
/*check out what you have learned from week 1 & 6*/
/*feel free to add your own function for convenience*/

/*===========================import variable===========================*/
int extern _Tp;
/*===========================import variable===========================*/

// Write the voltage to motor.
void MotorWriting(double vL, double vR) {
  // TODO: use L298N to control motor voltage & direction
}// MotorWriting

// Handle negative motor_PWMR value. 
void MotorInverter(int motor, bool& dir) {
  //Hint: the value of motor_PWMR must between 0~255, cannot write negative value.
}// MotorInverter

// P/PID control Tracking
void tracking(int l1,int l2,int l3,int r3,int r2,int r1){
  // find your own parameters!
  double _w1; // 
  double _w2; //
  double _w3; //
  double _Kp; // p term parameter 
  double _Kd; // d term parameter (optional) 
  double _Ki; // i term parameter (optional) (Hint: 不要調太大)
  double error=l1*_w1+l2*_w2+l3*_w3+r3*(-_w3)+r2*(-_w2)+r1*(-_w1);
  double vR, vL; // 馬達左右轉速原始值(從PID control 計算出來)。Between -255 to 255.
  double adj_R=1, adj_L=1; // 馬達轉速修正係數。MotorWriting(_Tp,_Tp)如果歪掉就要用參數修正。
    
  // TODO: complete your P/PID tracking code
  
  // end TODO
  MotorWriting(adj_L*vL, adj_R*vR);
}// tracking
