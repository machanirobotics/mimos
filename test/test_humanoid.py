import os
import pytest
import mimos as mi

mimos_mode = "test"
class SampleMimic:
    def __init__(self):
        pass

    def __call__(self, body):
        pass


def test_create_humanoid():
    body = mi.Body(
        skeleton=mi.skeleton.Blender(
            "blendfiles/Sample.blend", debug=True, mode=mimos_mode
        ),
    )
    # not passing body object
    with pytest.raises(TypeError):
        humanoid = mi.Humanoid()
        humanoid.run()
        assert humanoid is None

    # passing body object, no controller
    with pytest.raises(TypeError):
        humanoid = mi.Humanoid(body)
        humanoid.run()
        assert humanoid is None

    # passing both body and controller
    humanoid = mi.Humanoid(body, SampleMimic())
    humanoid.run()
    assert humanoid is not None
