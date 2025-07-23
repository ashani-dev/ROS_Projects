import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import Int32
import threading
import time



class DataShare:
        def __init__(self):
            self.x = 0.0
            self.az = 0.0
            self.lock = threading.Lock()
        


class JoystickListener(Node):
        def __init__(self, datashare):
            super().__init__('joystick_listener')
            self.subscription = self.create_subscription(
                Joy,
                'joy',
                self.joy_callback,
                1
            )
            self.subscription  # prevent unused variable warning
            self.datashare = datashare

  
            

        def joy_callback(self, msg):
            # Access joystick data from the 'msg' object
            # msg.axes contains a list of float values for joystick axes
            # msg.buttons contains a list of integer values (0 or 1) for buttons
            
            #get left joystick x or y axes, scale and send to datashare
            
            with self.datashare.lock:
                self.datashare.x = msg.axes[1] * 1
                self.datashare.az = msg.axes[0] * 0.5
                
            self.get_logger().info(f'Axes: {msg.axes}')
            #self.get_logger().info(f'Btzns: {msg.buttons}')


class TwistPublisher(Node):
    def __init__(self, datashare):
        super().__init__('twist_publisher')
        self.datashare = datashare
        self.publisher_ = self.create_publisher(Twist, '/model/rbot/cmd_vel', 10) # Topic: cmd_vel, QoS: 10
        timer_period = 0.2  # seconds
        self.timer = self.create_timer(timer_period, self.publish_twist_message)
        self.i = 0
        


    def publish_twist_message(self):
        x = 0.0
        az = 0.0
        with self.datashare.lock:
            x = self.datashare.x
            az = self.datashare.az
        twist_msg = Twist()
        twist_msg.linear.x = x  # Set linear velocity in x-direction
        twist_msg.angular.z = az  # Set angular velocity around z-axis
        self.publisher_.publish(twist_msg)
        #self.get_logger().info(f'Publishing Twist: linear.x={twist_msg.linear.x}, angular.z={twist_msg.angular.z}')
        self.i += 1
    

        
        
def main(args=None):
    rclpy.init(args=args)
    datashare = DataShare()
    joystick_listener = JoystickListener(datashare)
    twist_publisher = TwistPublisher(datashare)
    executor = MultiThreadedExecutor()
    executor.add_node(joystick_listener)
    executor.add_node(twist_publisher)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        joystick_listener.destroy_node()
        twist_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
