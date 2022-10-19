import sys

site_packages_paths = ${SITE_PACKAGES}
sys.path.extend(site_packages_paths)

from typing import Tuple
import zmq
import bpy
import json
import numpy as np


blender_config = open("src/mimos/controllers/mimic/config/blender.config.json")
class MimosClientOperator(bpy.types.Operator):
    bl_idname = "wm.mimos_client_operator"
    bl_label = "Mimos Client Operator"

    def __init__(self):
        self.zmq_ctx = zmq.Context()
        self.recv_sock = self.zmq_ctx.socket(zmq.SUB)
        self.recv_sock.bind(f"tcp://*:${STREAM_PORT}")
        self.recv_sock.setsockopt_string(zmq.SUBSCRIBE, "")

        # pass skeleton object name 
        self.skeleton_name = "${SKELETON_OBJECT}"
        self.skeleton = None
        self.timer = None

        # load bone config 
        self.bone_config = json.load(blender_config)
        self.bones = [bone['bone_name'] for bone in self.bone_config["bone_config"]]

    def modal(self, context, event):
        if event.type == "TIMER":
            # getting data from mimos
            frame_data = json.loads(self.recv_sock.recv_json())

            # getting the angles
            angles = frame_data.get("angles")

            # applying angles of each joint
            for joint_name, angle in angles.items():
                self.apply_angle(joint_name, angle)

        return {"PASS_THROUGH"}

    def execute(self, context):
        wm = context.window_manager
        # adding timer event for step of 0.04 secs
        self.timer = wm.event_timer_add(time_step=float(${MODAL_TIMER}), window=context.window)

        # initializing animation data
        self.skeleton = bpy.data.objects[self.skeleton_name]
        if not self.skeleton.animation_data:
            self.skeleton.animation_data_create()

        wm.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def apply_angle(self, bone_name: str, angle: Tuple[float, float, float]):
        bone = self.skeleton.pose.bones.get(bone_name, None)
        scale_x, scale_y, scale_z = 1,1,1
        if bone is not None and bone_name in self.bones:
            bone_info = [bone_ for bone_ in self.bone_config["bone_config"] if bone_['bone_name'] == bone_name]
            # scale_x, scale_y, scale_z = bone_info[0]["scale"]

            bone.rotation_euler.x = angle[0] # angle[1] * scale_y 
            bone.rotation_euler.y = angle[1] # angle[2] * scale_z 
            bone.rotation_euler.z = angle[2] # angle[0] * scale_x 

    def apply_location(self, bone_name: str, location):
        bone = self.skeleton.pose.bones.get(bone_name, None)
        scale_x, scale_y, scale_z = 1,1,1
        if bone is not None and bone_name in self.bones:
            bone_info = [bone_ for bone_ in self.bone_config["bone_config"] if bone_['bone_name'] == bone_name]
            scale_x, scale_y, scale_z = bone_info[0]["scale"]
            print(f"joint:{bone_name} location:{location}")
            bone.location.x = location[1] #* scale_y
            bone.location.y = location[2] #* scale_z
            bone.location.z = location[0] #* scale_x

def register():
    bpy.utils.register_class(MimosClientOperator)


def unregister():
    bpy.utils.unregister_class(MimosClientOperator)


if __name__ == "__main__":
    register()

    # executing and starting operator
    bpy.ops.wm.mimos_client_operator()
