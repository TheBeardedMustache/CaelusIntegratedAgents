import asyncio
from pathlib import Path

import streamlit as st

from desktop_app.app_state import STATE
from desktop_app.services.agent_manager import AgentManager
from archagents import ARCHAGENTS, load as load_arch, get_meta
from desktop_app.services.export_service import ExportService
from desktop_app.services.json_settings import JsonSettings

DEFAULT_INTENT = "default"

st.set_page_config(page_title="Caelus Agents", layout="wide")


def dashboard_page():
    st.header("Dashboard")
    st.write(STATE.stats if STATE.stats else "No stats yet")


def exports_page():
    st.header("Exports")
    service = ExportService()

    if st.button("Scan Now"):
        st.session_state.export_data = asyncio.run(service.scan_chatgpt())

    data = st.session_state.get("export_data", [])
    if data:
        fmt = st.selectbox("Format", ["docx", "pdf"], key="fmt")
        font = st.selectbox("Font", ["Arial", "Times New Roman"], key="font")
        selected = []
        for item in data:
            label = f"{item.get('title', '')} ({item.get('type', '')})"
            if st.checkbox(label, key=item.get("id")):
                selected.append(item.get("id"))
        if st.button("Export Selected") and selected:
            for item_id in selected:
                service.export(item_id, fmt, font)
            st.success("Export complete")
    else:
        st.write("No export data loaded.")


def agents_page():
    st.header("Agents")
    manager = AgentManager()
    agents = manager.list_agents()

    if not agents:
        st.info("No agents available")
        return

    names = [a.get("name", "") for a in agents]
    index = st.selectbox("Select Agent", range(len(names)), format_func=lambda i: names[i])
    agent = agents[index]

    st.write(agent.get("description", ""))
    st.write(f"Last run: {agent.get('last_run', 'N/A')}")

    if st.button("Run Now"):
        manager.run_agent(agent["name"], DEFAULT_INTENT)
        st.success("Agent executed")


def settings_page():
    st.header("Settings")
    settings = JsonSettings()
    data = settings.load()

    exports = st.text_input("Exports Folder", value=data.get("paths", {}).get("exports", ""))
    temp = st.text_input("Temp Folder", value=data.get("paths", {}).get("temp", ""))
    if st.button("Save"):
        data.setdefault("paths", {})["exports"] = exports
        data["paths"]["temp"] = temp
        settings.save(data)
        st.success("Settings saved")

    log_file = Path(__file__).resolve().parent / "desktop_app" / "logs" / "caelus.log"
    if log_file.exists():
        txt = log_file.read_bytes().decode("utf-8", errors="replace")
        st.text_area("Log", txt, height=300)


def main():
    page = st.sidebar.radio("Page", ["Dashboard", "Exports", "Agents", "Archagents", "Settings"])
    if page == "Dashboard":
        dashboard_page()
    elif page == "Exports":
        exports_page()
    elif page == "Agents":
        agents_page()
    elif page == "Archagents":
        st.header("🜂  Master Archagent Console")
        st.markdown("### Hierarchy")
        mgr = AgentManager()
        tree = mgr.arch_hierarchy()
        with st.container():
            st.json(tree, expanded=False)

        st.divider()
        for arch in ARCHAGENTS:
            with st.expander(f"{arch['glyph']}  **{arch['title']}** — {arch['mandate']}"):
                cols = st.columns([3,1,1])
                with cols[0]:
                    st.write(f"Child agents: `{', '.join(arch['child_agents'])}`")
                if cols[1].button("Run", key=f"run_{arch['id']}"):
                    res = mgr.run_agent(arch['id'], arch['default_intent'], target_id='demo')
                    st.success(res)
                if cols[2].button("Chat", key=f"chat_{arch['id']}"):
                    prompt = st.text_input("Your message:", key=f"msg_{arch['id']}")
                    if st.button("Send", key=f"send_{arch['id']}"):
                        result = load_arch(arch['id']).run(message=prompt)
                        st.info(result)
    else:
        settings_page()


if __name__ == "__main__":
    main()
