import mimos as mi
import pytest


def test_create_body():
    # pass in wrong file path
    with pytest.raises(FileNotFoundError):
        body = mi.Body(
            skeleton=mi.skeleton.Blender("blendfiles/Ria2.blend", debug=True),
        )
        assert body is None

    # pass in correct file path
    body = mi.Body(
        skeleton=mi.skeleton.Blender("blendfiles/Ria.blend", debug=True),
    )
    assert body is not None
