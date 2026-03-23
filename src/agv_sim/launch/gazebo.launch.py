import os
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('agv_sim')
    urdf_file = os.path.join(pkg_share, 'urdf', 'robotomni.urdf')

    # Read URDF content
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Robot State Publisher Node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # Ensure Gazebo knows where to find the package's meshes
    pkg_prefix = get_package_prefix('agv_sim')
    gazebo_model_path = os.path.join(pkg_prefix, 'share')
    env_var = SetEnvironmentVariable('GAZEBO_MODEL_PATH', gazebo_model_path)

    # Custom world file
    world_file = os.path.join(pkg_share, 'worlds', 'empty_mini.world')

    # Gazebo Launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
        launch_arguments={'world': world_file}.items()
    )

    # RViz2 Launch
    rviz_config_file = os.path.join(pkg_share, 'config', 'display.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
    )

    # Spawn Robot Node
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                   '-entity', 'robotomni',
                   '-z', '0.05'],  # Spawn slightly above ground
        output='screen'
    )

    return LaunchDescription([
        env_var,
        gazebo,
        robot_state_publisher_node,
        spawn_entity,
        rviz_node,
    ])
