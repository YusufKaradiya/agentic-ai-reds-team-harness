from core.tool_registry import ToolRegistry


def test_tools_are_loaded():

    registry = ToolRegistry(
        "configs"
    )

    tools = registry.list_tools()

    assert len(tools) == 4


def test_send_email_requires_approval():

    registry = ToolRegistry(
        "configs"
    )

    tool = registry.get_tool(
        "send_email"
    )

    assert tool.requires_approval is True


def test_disabled_tool():

    registry = ToolRegistry(
        "configs"
    )

    assert (
        registry.is_enabled(
            "delete_record"
        )
        is False
    )