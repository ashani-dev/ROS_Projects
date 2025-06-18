from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import get_package_share_directory
import os

def generate_launch_description():
	gazebo = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
			os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
		)
	)

	sdf_path = os.path.join(get_package_share_directory('rbot_description'), 'sdf', 'rbot.sdf')

	spawn_entity = Node(
		package='gazebo_ros',
		executable='spawn_entity.py',
		arguments=['-entity', 'rbot', '-file', sdf_path, '-sdf'],
		output='screen'
	)


	return LaunchDescription([
		gazebo,
		spawn_entity
	])
