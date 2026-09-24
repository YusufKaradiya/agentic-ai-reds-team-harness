import sys
from pathlib import Path

import streamlit as st
import pandas as pd

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.agent_controller import AgentController

st.set_page_config(
    page_title="Agentic AI Red-Team Harness",
    layout="wide"
)


@st.cache_resource
def get_controller():

    return AgentController(
        config_root=str(project_root / "configs"),
        database_path=str(project_root / "data" / "redteam.db"),
    )


controller = get_controller()

if "last_result" not in st.session_state:
    st.session_state.last_result = None

llm_available = controller.llm_service.available()

if llm_available:
    st.success("🟢 Ollama is connected")
else:
    st.error("🔴 Ollama is not available")


st.title(
    "🛡️ Agentic AI Red-Team Harness"
)

st.caption(
    "Prompt Injection • Tool Abuse • Data Exfiltration"
)


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Run Attack",
        "Attack Corpus",
        "Evaluation",
        "Audit Logs",
    ]
)


# ------------------------------------------------
# TAB 1
# ------------------------------------------------

with tab1:

    st.header("Run Security Test")

    attacks = controller.attack_loader.list_attacks()

    attack_map = {
        attack.id: attack
        for attack in attacks
    }

    attack_id = st.selectbox(
        "Select Attack",
        list(attack_map.keys())
    )

    attack = attack_map[attack_id]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Category",
            attack.category
        )

    with col2:
        st.metric(
            "Severity",
            attack.severity
        )

    with col3:
        st.metric(
            "Target",
            attack.target
        )

    st.write(
        "**Description:**",
        attack.description
    )

    st.write(
        "**Payload:**"
    )

    st.code(
        attack.payload
    )

    st.divider()

    mode = st.radio(
        "Execution Mode",
        [
            "Defense",
            "Baseline",
        ],
        horizontal=True
    )

    defense_enabled = (
        mode == "Defense"
    )

    tools = controller.tool_registry.list_tools()

    tool_options = [
        "No Tool"
    ] + [
        tool.id
        for tool in tools
    ]

    selected_tool = st.selectbox(
        "Optional Tool",
        tool_options
    )

    tool_id = (
        None
        if selected_tool == "No Tool"
        else selected_tool
    )

    user_approved = st.checkbox(
        "Approve high-risk tool if required"
    )

    if st.button(
        "🚀 Run Attack",
        type="primary"
    ):

        st.session_state.last_result = controller.run_attack(
            attack_id=attack_id,
            tool_id=tool_id,
            defense_enabled=defense_enabled,
            user_approved=user_approved,
        )

    st.subheader("LLM Information")

c1, c2, c3 = st.columns(3)

result = st.session_state.last_result

if result is None:
    st.info("Run an attack to see the LLM response.")
else:
    with c1:
        st.metric(
            "LLM Called",
            str(result["llm_called"])
        )

    with c2:
        st.metric(
            "LLM Model",
            result["llm_model"] or "N/A"
        )

    with c3:
        st.metric(
            "LLM Latency",
            f'{result["llm_latency_ms"]} ms'
        )

    if result["llm_output"]:

        st.subheader("LLM Output")

        st.write(
            result["llm_output"]
        )

        st.json(result)


# ------------------------------------------------
# TAB 2
# ------------------------------------------------

with tab2:

    st.header("Attack Corpus")

    attacks = controller.attack_loader.list_attacks()

    rows = []

    for attack in attacks:

        rows.append({
            "ID": attack.id,
            "Name": attack.name,
            "Category": attack.category,
            "Severity": attack.severity,
            "Target": attack.target,
            "Expected": getattr(
                attack,
                "expected_behavior",
                "N/A"
            ),
        })

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True
    )


# ------------------------------------------------
# TAB 3
# ------------------------------------------------

with tab3:

    st.header("Evaluation")

    runs = controller.database.get_runs()

    if not runs:

        st.info(
            "No experiments have been executed yet."
        )

    else:

        total = len(runs)

        attack_successes = sum(
            1
            for run in runs
            if run["attack_success"]
        )

        false_blocks = sum(
            1
            for run in runs
            if run["false_block"]
        )

        leakage = sum(
            1
            for run in runs
            if run["data_leakage"]
        )

        asr = attack_successes / total

        fbr = false_blocks / total

        leakage_rate = leakage / total

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Total Runs",
                total
            )

        with c2:
            st.metric(
                "Attack Success Rate",
                f"{asr:.2%}"
            )

        with c3:
            st.metric(
                "False Block Rate",
                f"{fbr:.2%}"
            )

        with c4:
            st.metric(
                "Leakage Rate",
                f"{leakage_rate:.2%}"
            )

        st.subheader(
            "Experiment Records"
        )

        st.dataframe(
            pd.DataFrame(runs),
            use_container_width=True
        )


# ------------------------------------------------
# TAB 4
# ------------------------------------------------

with tab4:

    st.header("Audit Logs")

    runs = controller.database.get_runs()

    events = controller.database.get_events()

    st.subheader("Runs")

    if runs:

        st.dataframe(
            pd.DataFrame(runs),
            use_container_width=True
        )

    else:

        st.info("No runs available.")

    st.subheader("Events")

    if events:

        st.dataframe(
            pd.DataFrame(events),
            use_container_width=True
        )

    else:

        st.info("No events available.")