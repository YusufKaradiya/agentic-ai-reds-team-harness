from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:
    tool_id: str
    success: bool
    output: str
    metadata: dict[str, Any]


class MockToolExecutor:
    """
    Executes isolated simulated tools.

    No real email, customer system or external service
    is contacted.
    """

    def execute(
        self,
        tool_id: str,
        parameters: dict[str, Any] | None = None,
    ) -> ToolResult:

        parameters = parameters or {}

        if tool_id == "search_customer":

            query = parameters.get(
                "query",
                "unknown"
            )

            return ToolResult(
                tool_id=tool_id,
                success=True,
                output=(
                    f"Mock customer search completed "
                    f"for query: {query}"
                ),
                metadata={
                    "simulated": True
                },
            )

        if tool_id == "get_account":

            return ToolResult(
                tool_id=tool_id,
                success=True,
                output=(
                    "Mock account data retrieved."
                ),
                metadata={
                    "simulated": True,
                    "contains_real_data": False,
                },
            )

        if tool_id == "send_email":

            recipient = parameters.get(
                "recipient",
                "unknown"
            )

            return ToolResult(
                tool_id=tool_id,
                success=True,
                output=(
                    f"Mock email prepared for {recipient}. "
                    "No real email was sent."
                ),
                metadata={
                    "simulated": True,
                    "external_action": False,
                },
            )

        if tool_id == "delete_record":

            return ToolResult(
                tool_id=tool_id,
                success=True,
                output=(
                    "Mock deletion operation executed."
                ),
                metadata={
                    "simulated": True,
                    "external_action": False,
                },
            )

        return ToolResult(
            tool_id=tool_id,
            success=False,
            output="Unknown mock tool.",
            metadata={
                "simulated": True
            },
        )