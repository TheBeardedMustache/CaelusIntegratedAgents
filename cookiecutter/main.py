from pathlib import Path
import shutil

def cookiecutter(template, no_input=True, extra_context=None, output_dir="."):
    extra_context = extra_context or {}
    slug = extra_context.get("agent_slug", "agent")
    agent_name = extra_context.get("agent_name", "Agent")
    template_path = Path(template)
    out = Path(output_dir) / slug
    src = template_path / "{{cookiecutter.agent_slug}}"
    shutil.copytree(src, out)
    for path in out.rglob("*"):
        if path.is_file():
            text = path.read_text()
            text = text.replace("{{cookiecutter.agent_slug}}", slug)
            text = text.replace("{{cookiecutter.agent_name}}", agent_name)
            path.write_text(text)
    return str(out)
