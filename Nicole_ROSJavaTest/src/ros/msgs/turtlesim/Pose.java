package ros.msgs.turtlesim;

/**
 * A Java Bean for the turtlesim/Pose ROS message type
 * @author NSC
 */
public class Pose {
	public float x;
	public float y;
	public float theta;
	public float linear_velocity;
	public float angular_velocity;

	public Pose(){}

	// public Pose(Vector3 linear, Vector3 angular) {
	// 	this.linear = linear;
	// 	this.angular = angular;
	// }
}
