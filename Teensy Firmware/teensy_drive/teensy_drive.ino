#include <ros.h>
#include <std_msgs/Bool.h>
#include <std_msgs/String.h>
#include <std_msgs/Int32.h>
#include <std_msgs/Empty.h>
#include <race/drive_values.h>
ros::NodeHandle nh;
boolean flagStop = false;
int pwm_center_value = 9780; // Center of safe stop region
int vel_lowerlimit = 9400; // Small range to limit velocity for a small room
int vel_upperlimit = 10160; // Same as above
int ang_lowerlimit = 7180; // Small range to limit velocity for a small room
int ang_upperlimit = 12380; // Same as above
//int vel_pwm = 9780; // Global pwm output val for velocity
std_msgs::Int32 str_msg;
ros::Publisher chatter("chatter", &str_msg);
int kill_pin = 2;
unsigned long duration = 0;

IntervalTimer velTmr;

void stopMotion(){ // Timer interrupt function
  analogWrite(5,pwm_center_value); // stop 
  velTmr.end();
}

void messageDrive( const race::drive_values& pwm ){
  //velTmr.end();
// Serial.print("Pwm drive : ");
// Serial.println(pwm.pwm_drive);
// Serial.print("Pwm angle : ");
// Serial.println(pwm.pwm_angle);
  if(flagStop == false){
    str_msg.data = pwm.pwm_drive;
    chatter.publish( &str_msg );
    if(pwm.pwm_drive < vel_lowerlimit){
        analogWrite(5,pwm_center_value); // stop
    }
    else if(pwm.pwm_drive > vel_upperlimit){
        analogWrite(5,pwm_center_value); // stop
    }
    else{
        analogWrite(5,pwm.pwm_drive);
        velTmr.begin(stopMotion,500000); // turn off the velocity in 0.5sec
//        analogWrite(5,pwm.pwm_drive); // Incoming data
    }
    if(pwm.pwm_angle < ang_lowerlimit) {
        analogWrite(6,pwm_center_value); // straight
    }
    else if(pwm.pwm_angle > ang_upperlimit){
        analogWrite(6,pwm_center_value); // straight
    }
    else{
        analogWrite(6,pwm.pwm_angle); // Incoming data
    }
  }
  else{
      analogWrite(5,pwm_center_value);
      analogWrite(6,pwm_center_value);
      digitalWrite(2,LOW);
  }
}
void messageEmergencyStop( const std_msgs::Bool& flag ){
  flagStop = flag.data;
  if(flagStop == true){
    analogWrite(5,pwm_center_value);
    analogWrite(6,pwm_center_value);
  }
}
ros::Subscriber<race::drive_values> sub_drive("drive_pwm", &messageDrive );
ros::Subscriber<std_msgs::Bool> sub_stop("eStop", &messageEmergencyStop );
void setup() {
  analogWriteFrequency(5, 100);
  analogWriteFrequency(6, 100);
  analogWriteResolution(16);
  analogWrite(5,pwm_center_value);
  analogWrite(6,pwm_center_value);
  pinMode(13,OUTPUT);
  digitalWrite(13,HIGH);
//  pinMode(2,INPUT);
//  digitalWrite(2,HIGH);
  nh.initNode();
  nh.subscribe(sub_drive);
  //nh.subscribe(sub_stop);
  nh.advertise(chatter);
}
void loop() {
  nh.spinOnce();
}
