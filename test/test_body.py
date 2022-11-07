import mimos as mi
import pytest
import os

# set MODE_ENV as test
mimos_mode = "test"


def test_create_body():
    # pass in wrong file path
    with pytest.raises(FileNotFoundError):
        body = mi.Body(
            skeleton=mi.skeleton.Blender(
                "blendfiles/sample2.blend", debug=True, mode=mimos_mode
            ),
        )
        assert body is None

    # pass in correct file path
    body = mi.Body(
        skeleton=mi.skeleton.Blender(
            "blendfiles/Sample.blend", debug=True, mode=mimos_mode
        ),
    )
    assert body is not None
