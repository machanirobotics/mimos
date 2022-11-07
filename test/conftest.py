import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--mode",
        action="store",
        default=[],
        help="list of stringinputs to pass to test functions",
    )


@pytest.fixture
def mimos_mode(request):
    return request.config.getoption("--mode")
