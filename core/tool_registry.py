from pathlib import Path

from core.config_loader import ConfigLoader
from core.contracts import ToolDefinition


class ToolRegistry:
    """
    Central registry for configured tools.
    """

    def __init__(self, config_root: str = "configs"):
        self.loader = ConfigLoader(
            Path(config_root)
        )

        data = self.loader.load_tools()

        self.tools = {
            item["id"]: ToolDefinition.model_validate(item)
            for item in data.get("tools", [])
        }

    def list_tools(self) -> list[ToolDefinition]:
        return list(self.tools.values())

    def get_tool(
        self,
        tool_id: str
    ) -> ToolDefinition:

        if tool_id not in self.tools:
            raise KeyError(
                f"Unknown tool: {tool_id}"
            )

        return self.tools[tool_id]

    def is_enabled(
        self,
        tool_id: str
    ) -> bool:

        tool = self.get_tool(tool_id)

        return tool.enabled