import pytest

from {{cookiecutter.agent_slug}} import Agent


def test_run_not_implemented():
    agent = Agent()
    with pytest.raises(NotImplementedError):
        agent.run()
