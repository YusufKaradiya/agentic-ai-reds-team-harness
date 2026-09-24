from core.config_loader import ConfigLoader
from core.contracts import ToolDefinition


class ToolRegistry:

    def __init__(
        self,
        config_path="configs/attacks/tools.yaml"
    ):

        config_path = ConfigLoader(config_path).config_root
        if config_path.is_dir():
            config_path = config_path / "attacks" / "tools.yaml"

        loader = ConfigLoader(config_path)

        data = loader.load()

        self.tools = {}

        for item in data.get(
            "tools",
            []
        ):

            tool = ToolDefinition.model_validate(
                item
            )

            self.tools[
                tool.id
            ] = tool

    def list_tools(self):

        return list(
            self.tools.values()
        )

    def get_tool(self, tool_id):

        return self.tools.get(
            tool_id
        )

    def is_enabled(self, tool_id):

        tool = self.get_tool(
            tool_id
        )

        return (
            tool is not None
            and tool.enabled
        )