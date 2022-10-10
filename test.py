import mimos as mi

body = mi.Body(
    skeleton=mi.skeleton.Blender(
        "/home/rohan/Desktop/mrobotics/mimos/blendfiles/Ria.blend", debug=True
    ),
)


body.animate("namaste")
body.animate("l_stand_hello")
# body.speak("hello")

# body.do(
#     mi.animate("dance-1"),
#     mi.speak("hello"),
#     mi.parallel(
#         mi.animate("dance-3"),
#         mi.speak("hello"),
#     ),
# )

# body.speak("im done")


# class Mimic:
#     def __call__(self, body):
#         # for frame in body.see():
#         #     cv2.imshow("frame", frame)
#         #     cv2.waitKey(1)
#         pass


# humanoid = mi.Humanoid(body=body, controller=Mimic())
# humanoid.run()
