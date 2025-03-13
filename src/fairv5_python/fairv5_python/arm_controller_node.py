import rclpy
from rclpy.node import Node
from moveit_msgs.srv import GetPositionIK
from moveit_msgs.msg import MotionPlanRequest, JointConstraint, Constraints
from moveit_msgs.action import MoveGroup
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
from tf2_ros import TransformListener, Buffer
import math

class MoveRobot(Node):
    def __init__(self):
        super().__init__('move_robot_to_target')
        
        # MoveIt 2 Action Client
        self.move_group_client = ActionClient(self, MoveGroup, 'move_action')
        
        # Joint Trajectory Action Client
        self.trajectory_client = ActionClient(self, FollowJointTrajectory, '/arm_controller/follow_joint_trajectory')
        
        # TF2 Listener for current robot state
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.get_logger().info("MoveRobot node initialized.")

    def move_to_target(self, target_joint_positions):
        """
        Move the robot to the target joint positions.
        :param target_joint_positions: List of target joint positions [j1, j2, j3, j4, j5, j6]
        """
        # Create a JointTrajectory message
        trajectory_msg = JointTrajectory()
        trajectory_msg.joint_names = ['j1', 'j2', 'j3', 'j4', 'j5', 'j6']
        
        # Create a trajectory point
        point = JointTrajectoryPoint()
        point.positions = target_joint_positions
        point.time_from_start.sec = 5  # 5 seconds to reach the target
        
        trajectory_msg.points.append(point)
        
        # Create a FollowJointTrajectory goal
        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory = trajectory_msg
        
        # Send the goal
        self.get_logger().info("Sending trajectory goal...")
        self.trajectory_client.wait_for_server()
        future = self.trajectory_client.send_goal_async(goal_msg)
        future.add_done_callback(self.trajectory_goal_response_callback)

    def trajectory_goal_response_callback(self, future):
        """
        Callback for trajectory goal response.
        """
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error("Trajectory goal rejected.")
            return
        
        self.get_logger().info("Trajectory goal accepted.")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.trajectory_result_callback)

    def trajectory_result_callback(self, future):
        """
        Callback for trajectory result.
        """
        result = future.result().result
        if result.error_code == result.SUCCESSFUL:
            self.get_logger().info("Trajectory execution succeeded.")
        else:
            self.get_logger().error(f"Trajectory execution failed with error code: {result.error_code}")

def main(args=None):
    rclpy.init(args=args)
    
    # Target joint positions (example values)
    target_joint_positions = [0.5, -0.5, 0.5, -0.5, 0.5, -0.5]  # Replace with your desired joint positions
    
    move_robot_node = MoveRobot()
    move_robot_node.move_to_target(target_joint_positions)
    
    rclpy.spin(move_robot_node)
    move_robot_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()