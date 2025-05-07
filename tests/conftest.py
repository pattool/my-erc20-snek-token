import pytest
from script.deploy import deploy


@pytest.fixture(scope="function")
def snek_token():
    return deploy()