#include <ros.h>
#include <sensor_msgs/Imu.h>
#include <SparkFunMPU9250-DMP.h>

#define SerialPort SerialUSB

MPU9250_DMP imu;

ros::NodeHandle nh;
sensor_msgs::Imu my_msg;

ros::Publisher pos_pub("imu0", &my_msg);

// Need to publish to topic /imu0 
// Data type is sensor_msgs/Imu

void setup() {
  
  
  SerialPort.begin(115200);

  // Call imu.begin() to verify communication and initialize
  if (imu.begin() != INV_SUCCESS) {
     while (1) {
      SerialPort.println("Unable to communicate with MPU-9250");
      SerialPort.println("Check connections, and try again");
      SerialPort.println();
      delay(5000);
     }
  }

  imu.setSensors(INV_XYZ_GYRO | INV_XYZ_ACCEL | INV_XYZ_COMPASS);

  imu.setGyroFSR(2000); // Set gyro to 2000dps
  imu.setAccelFSR(2);   // Set accel to +/-2g
  imu.setLPF(5); // Set LPF corner frequency to 5Hz
  imu.setSampleRate(10);
  imu.setCompassSampleRate(10);
  // Enable 6-axis quat and use gyro calibration
  // Set DMP FIFO rate to 10Hz
  imu.dmpBegin(DMP_FEATURE_6X_LP_QUAT | 
               DMP_FEATURE_GYRO_CAL,
               10);
  nh.initNode();
  nh.advertise(pos_pub);
  
}

void loop() {

  // Check for new data in the FIFO
  if (imu.fifoAvailable()) {
     // Use dmpUpdateFifo to update the ax, gx, mx, etc. values
     if ( imu.dmpUpdateFifo() == INV_SUCCESS ) {
       // computeEulerAngles can be used -- after updating the 
       // quaternion values -- to estimate roll, pitch and yaw
       imu.update(UPDATE_ACCEL | UPDATE_GYRO | UPDATE_COMPASS);
       imu.computeEulerAngles();
       createMsgQuaternion();
       createMsgAngVelAndLinAcc();
       pos_pub.publish(&my_msg);
     }
  }
  nh.spinOnce();
}

void createMsgQuaternion(void) {
   // After calling dmpUpdateFifo() the ax, gx, mx, etc. values
   // are all updated.
   // Quaternion values are, by default, stored in long format
   // calcQuat turns them into a float between -1 and 1
   float q0 = imu.calcQuat(imu.qw);
   float q1 = imu.calcQuat(imu.qx);
   float q2 = imu.calcQuat(imu.qy);
   float q3 = imu.calcQuat(imu.qz);

   my_msg.orientation.x = q0;
   my_msg.orientation.y = q1;
   my_msg.orientation.z = q2;
   my_msg.orientation.w = q3;
}

void createMsgAngVelAndLinAcc(void) {
    float accelX = imu.calcAccel(imu.ax);
    float accelY = imu.calcAccel(imu.ay);
    float accelZ = imu.calcAccel(imu.az);
    float gyroX = imu.calcAccel(imu.gx);
    float gyroY = imu.calcAccel(imu.gy);
    float gyroZ = imu.calcAccel(imu.gz);

    my_msg.linear_acceleration.x = accelX;
    my_msg.linear_acceleration.y = accelY;
    my_msg.linear_acceleration.z = accelZ;

    my_msg.angular_velocity.x = gyroX;
    my_msg.angular_velocity.y = gyroY;
    my_msg.angular_velocity.z = gyroZ;
    
}
