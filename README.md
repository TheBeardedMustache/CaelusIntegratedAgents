# Caelus Integrated Agents

## Building the Desktop App

```bash
python -m venv .venv && .venv/"$(test "$(uname -s)" = "Darwin" && echo bin || echo Scripts)"/activate
pip install -r requirements.txt pyinstaller pyside6
pyinstaller CaelusIntegratedAgents.spec
```

### Linux Prerequisites

The bundled application requires `libEGL.so.1` and `libxkbcommon-x11.so.0` at runtime. Install them with:

```bash
sudo apt-get update
sudo apt-get install -y libegl1 libxkbcommon-x11-0
```

After building, run the executable from the `dist/` directory.

### Custom Logging Configuration

Set the `CAELUS_LOGGING_CONFIG` environment variable to the path of a YAML file
to override the default logging setup.
