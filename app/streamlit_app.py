from pathlib import Path
import sys

import streamlit as st


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from core.agent_controller import AgentController
from core.attack_loader import AttackLoader
from core.tool_registry import ToolRegistry


st.set_page_config(
    page_title="Agentic AI Red-Team Harness",
    page_icon="🛡️",
    layout="wide",
)


@st.cache_resource
def get_controller(cache_version: int = 2):

    return AgentController(
        config_root="configs",
        database_path="data/redteam.db",
    )


@st.cache_resource
def get_attack_loader():

    return AttackLoader(
        "configs"
    )


@st.cache_resource
def get_tool_registry():

    return ToolRegistry(
        "configs"
    )


controller = get_controller(cache_version=2)
attack_loader = get_attack_loader()
tool_registry = get_tool_registry()


st.title(
    "🛡️ Agentic AI Red-Team Harness"
)

st.caption(
    "Prompt Injection • Tool Abuse • Data Exfiltration"
)

st.divider()


tab1, tab2, tab3 = st.tabs(
    [
        "Run Attack",
        "Attack Corpus",
        "Audit Logs",
    ]
)


# =========================================================
# TAB 1
# =========================================================

with tab1:

    st.header("Run Security Test")

    attacks = attack_loader.list_attacks()

    attack_map = {
        attack.id: attack
        for attack in attacks
    }

    selected_attack_id = st.selectbox(
        "Select Attack Scenario",
        options=list(attack_map.keys()),
    )

    selected_attack = attack_map[
        selected_attack_id
    ]

    st.subheader(
        selected_attack.name
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Category",
            selected_attack.category.value,
        )

    with col2:

        st.metric(
            "Severity",
            selected_attack.severity.value,
        )

    with col3:

        st.metric(
            "Target",
            selected_attack.target,
        )

    st.write(
        selected_attack.description
    )

    with st.expander(
        "View attack payload"
    ):

        st.code(
            selected_attack.payload,
            language="text",
        )

    st.subheader(
        "Optional Tool Test"
    )

    tool_options = ["None"]

    tool_options.extend(
        [
            tool.id
            for tool in
            tool_registry.list_tools()
        ]
    )

    selected_tool = st.selectbox(
        "Tool",
        options=tool_options,
    )

    tool_id = (
        None
        if selected_tool == "None"
        else selected_tool
    )

    if st.button(
        "▶ Run Security Test",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner(
            "Running security test..."
        ):

            result = controller.run_attack(
                attack_id=selected_attack_id,
                tool_id=tool_id,
            )

        st.success(
            "Security test completed."
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Decision",
                result["decision"],
            )

        with col2:

            st.metric(
                "Risk Score",
                result["risk_score"],
            )

        with col3:

            st.metric(
                "Latency",
                f'{result["latency_ms"]} ms',
            )

        with col4:

            st.metric(
                "Tool Called",
                str(result["tool_called"]),
            )

        st.subheader(
            "Execution Result"
        )

        st.json(result)


# =========================================================
# TAB 2
# =========================================================

with tab2:

    st.header(
        "Configured Attack Corpus"
    )

    attacks = attack_loader.list_attacks()

    for attack in attacks:

        with st.expander(
            f"{attack.id} — {attack.name}"
        ):

            st.write(
                f"**Category:** "
                f"{attack.category.value}"
            )

            st.write(
                f"**Severity:** "
                f"{attack.severity.value}"
            )

            st.write(
                f"**Target:** "
                f"{attack.target}"
            )

            st.write(
                attack.description
            )

            st.code(
                attack.payload
            )


# =========================================================
# TAB 3
# =========================================================

with tab3:

    st.header(
        "Audit Logs"
    )

    runs = controller.database.get_runs(
        limit=50
    )

    if runs:

        st.dataframe(
            runs,
            use_container_width=True,
        )

    else:

        st.info(
            "No security tests have been executed yet."
        )

    st.subheader(
        "Detailed Events"
    )

    events = controller.database.get_events(
        limit=100
    )

    if events:

        st.dataframe(
            events,
            use_container_width=True,
        )

    else:

        st.info(
            "No audit events available."
        )