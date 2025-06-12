import pytest

from exporter import Agent


def test_run_not_implemented():
    agent = Agent()
    with pytest.raises(NotImplementedError):
        agent.run()
