from queue import SimpleQueue
import zmq
import bpy
import time
from threading import Thread
import json

# bpy utils #
def initialize_blender(object: str):
    context = bpy.context
    obj = bpy.data.objects[object]
    bones = obj.pose.bones
    # create the animation data if it doesn't exist
    if not obj.animation_data:
        obj.animation_data_create()
    return (context, obj, bones)


def apply_angle(obj, bone: str, joint_angle: list):
    if bone in obj.pose.bones.keys():
        boneobj = obj.pose.bones[bone]
        boneobj.rotation_euler = joint_angle
    else:
        print(f"Bone {bone} not found in {obj}")


def run(joint_name: str, joint_angle: list):
    initialize_blender("BODY_Bones")
    obj = bpy.data.objects["BODY_Bones"]
    apply_angle(obj, joint_name, joint_angle)


class GenericOperator(bpy.types.Operator):
    bl_idname = "wm.generic_operator"
    bl_label = "Minimal Operator"

    def __init__(self):
        # connect to zmq socket
        self.ctx = zmq.Context()
        self.recv_sock = self.ctx.socket(zmq.SUB)
        self.recv_sock.bind("tcp://*:6666")
        self.recv_sock.setsockopt_string(zmq.SUBSCRIBE, "")

    def modal(self, context, event):
        if event.type in {"ESC", "RIGHTMOUSE"}:
            self.cancel(context)
            return {"FINISHED"}
        if event.type == "TIMER":
            frame_data = json.loads(self.recv_sock.recv_json())
            angles = frame_data.get("angles")
            for joint_name, angle in angles.items():
                run(joint_name, angle)
        return {"PASS_THROUGH"}

    def execute(self, context):
        wm = context.window_manager
        # adding timer event for step of 0.04 secs
        self._timer = wm.event_timer_add(time_step=0.04, window=context.window)
        wm.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def __del__(self):
        pass


bpy.utils.register_class(GenericOperator)
bpy.ops.wm.generic_operator()
