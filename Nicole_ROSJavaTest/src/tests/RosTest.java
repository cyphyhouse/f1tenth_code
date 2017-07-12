package tests;

import com.fasterxml.jackson.databind.JsonNode;
import ros.Publisher;
import ros.RosBridge;
import ros.RosListenDelegate;
import ros.SubscriptionRequestMsg;
import ros.msgs.std_msgs.PrimitiveMsg;
import ros.msgs.geometry_msgs.Twist;
import ros.msgs.geometry_msgs.Vector3;
import ros.msgs.turtlesim.Pose;
import ros.tools.MessageUnpacker;
import java.util.*;

/**
 * Example of connecting to rosbridge with publish/subscribe messages. Takes one argument:
 * the rosbridge websocket URI; for example: ws://localhost:9090.
 * @author James MacGlashan.
 */
public class RosTest {

    public static void main(String[] args) {

        if(args.length != 1){
            System.out.println("Need the rosbridge websocket URI provided as argument. For example:\n\tws://localhost:9090");
            System.exit(0);
        }

        // Initialize keyboard input value to 0 (no key pressed)
        // PrimitiveMsg<Integer> key_msg = new PrimitiveMsg<Integer>(0);
        // // Other ROS msg objects
        // // Pose pos_msg = new Pose();
        // Twist twist_msg = new Twist();

        RosBridge bridge = new RosBridge();
        bridge.connect(args[0], true);

        // Now need to add each subscriber to the arraylist of flags (maybe can be done in constructor)
        bridge.msgRxFlags.addAll(Arrays.asList(new Boolean[2]));

        bridge.subscribe(SubscriptionRequestMsg.generate("/keyboard_input")
                      .setType("std_msgs/Int32")
                      .setThrottleRate(1)
                      .setQueueLength(1),
                new RosListenDelegate() {

                      public void receive(JsonNode data, String stringRep, ArrayList<Boolean> flags) {
                            flags.set(0,true);                         
                      }
                }
        );

        bridge.subscribe(SubscriptionRequestMsg.generate("/turtle1/pose")
                    .setType("turtlesim/Pose")
                    .setThrottleRate(1)
                    .setQueueLength(1),
                new RosListenDelegate() {

                    public void receive(JsonNode data, String stringRep, ArrayList<Boolean> flags) {
                        flags.set(1,true); 
                    }
                }
        );

        // Publisher pub = new Publisher("/turtleX/cmd_vel", "geometry_msgs/Twist", bridge);

        // switch(key_msg.data){
        //     case 1: pub.publish(new Twist(new Vector3(1,0,0),new Vector3(0,0,0))); // Up key
        //     case 2: pub.publish(new Twist(new Vector3(0,0,0),new Vector3(1,1,0))); // Right key
        //     case 3: pub.publish(new Twist(new Vector3(-1,0,0),new Vector3(0,0,0))); // Down key
        //     case 4: pub.publish(new Twist(new Vector3(0,0,0),new Vector3(-1,-1,0))); // Left key
        //     default: pub.publish(new Twist(new Vector3(0,0,0),new Vector3(0,0,0))); // Stop
        // }

        // try {
        //     Thread.sleep(500);
        // } catch (InterruptedException e) {
        //     e.printStackTrace();
        // }
        while(true){

        }
    }

}
