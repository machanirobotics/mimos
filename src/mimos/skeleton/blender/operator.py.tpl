import sys

site_packages_paths = ${SITE_PACKAGES}
sys.path.extend(site_packages_paths)

from typing import Tuple
import zmq
import bpy
import json


class MimosClientOperator(bpy.types.Operator):
    bl_idname = "wm.mimos_client_operator"
    bl_label = "Mimos Client Operator"

    def __init__(self):
        self.zmq_ctx = zmq.Context()
        self.recv_sock = self.zmq_ctx.socket(zmq.SUB)
        self.recv_sock.bind(f"tcp://*:${STREAM_PORT}")
        self.recv_sock.setsockopt_string(zmq.SUBSCRIBE, "")

        # pass skeleton object name 
        self.skeleton_name =  "${SKELETON_OBJECT}"
        self.skeleton = None
        self.timer = None

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
        if bone is not None:
            bone.rotation_euler = angle
        else:
            print(f"bone {bone_name} not found")


def register():
    bpy.utils.register_class(MimosClientOperator)


def unregister():
    bpy.utils.unregister_class(MimosClientOperator)


if __name__ == "__main__":
    register()

    # executing and starting operator
    bpy.ops.wm.mimos_client_operator()
