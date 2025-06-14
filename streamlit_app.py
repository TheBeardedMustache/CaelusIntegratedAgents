# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

from archagents import ARCHAGENTS as _ARCHAGENTS, load as load_arch
# make sure ARCHAGENTS is a list, even if the package emitted a dict-based schema
if isinstance(_ARCHAGENTS, dict):
    ARCHAGENTS = _ARCHAGENTS.get("agents", [])
else:
    ARCHAGENTS = _ARCHAGENTS
from desktop_app.services.agent_manager import AgentManager
from awesome_loader import discover_extra_agents

st.set_page_config(page_title="Caelus Integrated Agents", layout="wide")

# -----------------------------------------------------------------------------
# Style tweaks
st.markdown(
    """
    <style>
      section[data-testid="stSidebar"] button {
        width: 100%;
        margin: 6px 0 !important;
        border-radius: 6px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Sidebar navigation
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ── Sidebar buttons (replace labels) ────────────────────────
HOME_ICON = "\U0001F3E0"   # 🏠 House
GEAR_ICON = "\u2699"       # ⚙ Gear

if st.sidebar.button(f"{HOME_ICON}  Dashboard"):
    st.session_state.page = "Dashboard"
if st.sidebar.button(f"{GEAR_ICON}  Settings"):
    st.session_state.page = "Settings"

# -----------------------------------------------------------------------------
# Dashboard page

def dashboard_page() -> None:
    st.header("\U0001F702  Seraph Control\xa0Center")

    # Chat area ---------------------------------------------------------------
    if "seraph_history" not in st.session_state:
        st.session_state.seraph_history = []

    chat_container = st.container()
    for msg in st.session_state.seraph_history:
        chat_container.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Ask Seraph…")
    if user_input:
        st.session_state.seraph_history.append({"role": "user", "content": user_input})
        seraph = load_arch("seraph")
        response = seraph.run(message=user_input)
        st.session_state.seraph_history.append({"role": "assistant", "content": str(response)})
        chat_container.chat_message("assistant").write(response)

    st.divider()

    # Archagents & Agents Overview ------------------------------------------
    mgr = AgentManager()
    extra = discover_extra_agents()
    all_archs = ARCHAGENTS + extra["archagents"]
    all_agents = mgr.list_agents() + extra["agents"]

    for arch in all_archs:
        with st.expander(f"{arch['glyph']} **{arch['title']}** — {arch['mandate']}"):
            st.write(f"Child agents: `{', '.join(arch['child_agents'])}`")
            col1, col2 = st.columns(2)
            if col1.button("Run", key=f"run_{arch['id']}"):
                result = mgr.run_agent(arch["id"], arch["default_intent"], target_id="demo")
                st.success(result)
            if col2.button("Schedule", key=f"sch_{arch['id']}"):
                st.info("Scheduler wiring TBD")

    st.divider()
    st.subheader("Choir Agents")
    for ag in all_agents:
        st.write(f"* **{ag['name']}** — _{ag.get('description','')}_")

# -----------------------------------------------------------------------------
# Settings page retains simple log viewer

def settings_page() -> None:
    st.header("Logs")
    log_file = Path("desktop_app/logs/caelus.log")
    if log_file.exists():
        txt = log_file.read_bytes().decode("utf-8", errors="replace")
        st.text_area("Log", txt, height=300)
    else:
        st.info("No log file yet.")

# -----------------------------------------------------------------------------
# Router

page = st.session_state.page
if page == "Dashboard":
    dashboard_page()
else:
    settings_page()
