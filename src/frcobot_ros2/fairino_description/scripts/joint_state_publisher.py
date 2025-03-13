#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from sensor_msgs.msg import JointState
from fairino_msgs.msg import RobotNonrtState

class JointStatePublisher(Node):
    def __init__(self):
        super().__init__('joint_state_publisher')
        
        # Başlangıçta eklem pozisyonları sözlüğü
        self.joint_positions = {
            'j1': 0.0,
            'j2': 0.0,
            'j3': 0.0,
            'j4': 0.0,
            'j5': 0.0,
            'j6': 0.0
        }
        
        # RobotNonrtState mesaj tipindeki topiğe abone olunuyor.
        # 'robot_state_topic' ifadesini, robotunuzun durum mesajını yayınladığı topik adıyla değiştirmeyi unutmayın.
        self.create_subscription(
            RobotNonrtState,
            'nonrt_state_data',
            self.robot_state_callback,
            10
        )
        
        # Gelen joint verilerini /joint_states topiğine yayınlamak için JointState publisher'ı oluşturuluyor.
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.00001, self.publish_states)
        
    def robot_state_callback(self, msg: RobotNonrtState):
        # Robot durum mesajından ilgili joint konumlarını güncelle
        self.joint_positions['j1'] = math.radians(msg.j1_cur_pos)
        self.joint_positions['j2'] = math.radians(msg.j2_cur_pos)
        self.joint_positions['j3'] = math.radians(msg.j3_cur_pos)
        self.joint_positions['j4'] = math.radians(msg.j4_cur_pos)
        self.joint_positions['j5'] = math.radians(msg.j5_cur_pos)
        self.joint_positions['j6'] = math.radians(msg.j6_cur_pos)
        self.get_logger().debug(
            f'Güncellenen eklem konumları: {self.joint_positions}'
        )
        
    def publish_states(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        # Joint isimleri ve pozisyonları sözlükten alınır
        msg.name = list(self.joint_positions.keys())
        msg.position = list(self.joint_positions.values())
        self.publisher.publish(msg)
        self.get_logger().info(f'Published JointState: {msg.position}')

def main(args=None):
    rclpy.init(args=args)
    node = JointStatePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
