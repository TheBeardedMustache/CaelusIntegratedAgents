import pytest

from squarespace_sync import Agent


def test_run_not_implemented():
    agent = Agent()
    with pytest.raises(NotImplementedError):
        agent.run()
