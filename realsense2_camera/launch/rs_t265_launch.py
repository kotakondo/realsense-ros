# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# DESCRIPTION #
# ----------- #
# Use this launch file to launch a t265 device.
# command line example:
# ros2 launch realsense2_camera rs_t265_launch.py

# The Parameters available for definition in the command line are described in rs_launch.configurable_parameters
# For example: to disable fisheye sensors:
# ros2 launch realsense2_camera rs_t265_launch.py enable_fisheye1:=false enable_fisheye2:=false

"""Launch realsense2_camera node."""
import copy
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.actions import PushRosNamespace
from launch.substitutions import LaunchConfiguration, ThisLaunchFileDir
from launch.launch_description_sources import PythonLaunchDescriptionSource
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()))
import rs_launch

t265_parameters = [
    {'name': 'device_type', 'default': 't265', 'description': 'choose device by type'},
    {'name': 'enable_pose', 'default': 'true', 'description': 'enable pose stream'},
    {'name': 'enable_fisheye1', 'default': 'true', 'description': 'enable fisheye1 stream'},
    {'name': 'enable_fisheye2', 'default': 'true', 'description': 'enable fisheye2 stream'},
    {'name': 'camera_name', 'default': 't265', 'description': 'camera unique name'},
]

def generate_launch_description():

    # Declare the namespace as a launch argument
    namespace_arg = DeclareLaunchArgument(
        'namespace',
        default_value='RR01',
        description='Namespace to launch the realsense2_camera node under'
    )

    # Get the namespace from the launch configuration
    namespace = LaunchConfiguration('namespace')

    # Push the namespace for all nodes in this launch file
    namespace_push = PushRosNamespace(namespace)

    # T265
    return LaunchDescription(
        [
            namespace_arg,
            namespace_push,
        ] +
        rs_launch.declare_configurable_parameters(t265_parameters) +
        [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([ThisLaunchFileDir(), '/rs_launch.py']),
                launch_arguments=rs_launch.set_configurable_parameters(t265_parameters).items(),
            ),
        ]
    )
