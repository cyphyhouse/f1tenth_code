launch files for hector slam:
hector_slam.launch starts up transform node to convert base frame to laser and hector_mapping node to take raw lidar data (of type LaserScan msg) and create an occupancy grid map. Map is published on the /map topic. 
If using real-time lidar data, set value to "false" in the "/use_sim_time" parameter. 
If using bagged data, set value to "true" and run rosbag play on separate terminal using "--clock" parameter. Eg: "rosbag play data.bag --clock"

Make sure "frame names" section in mapping_default.launch matches the names defined in the transform node that is launched from hector_slam.launch
