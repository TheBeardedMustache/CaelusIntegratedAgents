import asyncio
from pathlib import Path

import streamlit as st

from desktop_app.app_state import STATE
from desktop_app.services.agent_manager import AgentManager
from archagents import ARCHAGENTS
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
        st.text_area("Log", log_file.read_text(encoding="utf-8"), height=300)


def main():
    page = st.sidebar.radio("Page", ["Dashboard", "Exports", "Agents", "Archagents", "Settings"])
    if page == "Dashboard":
        dashboard_page()
    elif page == "Exports":
        exports_page()
    elif page == "Agents":
        agents_page()
    elif page == "Archagents":
        st.header("Master Archagent Console")
        manager = AgentManager()
        for arch in ARCHAGENTS:
            with st.expander(f"{arch['glyph']}  {arch['title']}"):
                st.write(arch["mandate"])
                st.write("Child agents: " + ", ".join(arch["child_agents"]))
                col1, col2 = st.columns(2)
                if col1.button("Run Now", key=f"run_{arch['id']}"):
                    manager.run_agent(arch["id"], arch["default_intent"], target_id="demo")
                    st.success("Invocation dispatched")
                cron = col2.text_input("Cron (e.g. 0 9 * * *)", key=f"cron_{arch['id']}")
                if col2.button("Schedule", key=f"sch_{arch['id']}") and cron:
                    manager.schedule_agent(arch["id"], arch["default_intent"], cron)
                    st.info("Scheduled")
    else:
        settings_page()


if __name__ == "__main__":
    main()
