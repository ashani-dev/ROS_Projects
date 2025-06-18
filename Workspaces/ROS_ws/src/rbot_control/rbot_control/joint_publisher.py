import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from gazebo_msgs.srv import GetJointProperties

class JointPublisher(Node):
    def __init__(self):
        super().__init__('joint_publisher')
        self.publisher = self.create_publisher( 
            JointState,
            'rbot/joint_states',
            self.listener_callback,
            10
        )
        self.client = self.create_client(GetJointProperties, '/gazebo/get_joint_properties')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /gazebo/get_joint_properties service...')
        self.joint_names = ['left_wheel_joint', 'right_wheel_joint']
        self.timer = self.create_timer(0.1, self.timer_callback)
    
    def timer_callback(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = []
        
        for joint in self.joint_names:
            req = GetJointProperties.Request()
            req.joint_name = joint
            future = self.client.call_async(req)
            rclpy.spin_until_future_complete(self,future)
            if future.result():
                msg.position.append(future.result().position[0])
            else:
                self.get_logger().error('Failed to call service')
                msg.position.append(0.0)
                
        self.publisher_.publish(msg)
            
def main(args=None):
    rclpy.init(args=args)
    node = JointPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
     
