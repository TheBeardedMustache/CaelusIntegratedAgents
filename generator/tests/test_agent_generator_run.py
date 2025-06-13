from pathlib import Path

from generator.agent_generator import AgentGenerator


def test_agent_generator_run(tmp_path):
    gen = AgentGenerator()
    folder = gen.run(
        "caelus-agent",
        {"agent_name": "Foo Agent", "agent_slug": "foo_agent"},
        output_dir=tmp_path,
    )

    generated = Path(folder)
    assert generated.exists()
    assert generated.name == "foo_agent"
    assert (generated / "agent.py").exists()
    assert (generated / "tests" / "test_basic.py").exists()
    assert generated.parent == tmp_path
