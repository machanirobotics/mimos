import mimos as mi
import pytest
import os

# set MODE_ENV as test
mimos_mode = ""
env_file = os.getenv("GITHUB_ENV")
with open(env_file, "r") as f:
    for line_number, line in enumerate(f, start=1):
        if "MODE_ENV" in line:
            mimos_mode = line.split("=")[1].strip()
            print("current mimos_mode is ", mimos_mode)
            break


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
