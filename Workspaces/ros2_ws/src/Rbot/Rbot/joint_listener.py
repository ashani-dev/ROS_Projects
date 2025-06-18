import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class JointListener(Node):
    def __init__(self):
        super().__init__('joint_listener')
        self.subscription = self.create_subscription(
            JointState,
            'rbot/joint_states',
            self.listener_callback,
            10
        )
        
    def listener_callback(self, msg):
        for name, pos in zip(msg.name, msg.position):
            self.get_logger().info(f'{name}: {pos:.3f}')
            
def main(args=None):
    rclpy.init(args=args)
    node = JointListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    
