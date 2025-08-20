from typing import Any, Dict, List

from langchain_core.callbacks import BaseCallbackHandler


class TranscriptCallbackHandler(BaseCallbackHandler):
    """Collect a human-readable transcript of an agent run.

    Captures tool invocations and outputs similar to verbose=True console logs,
    so we can return them to clients alongside the final answer.
    """

    def __init__(self) -> None:
        self._lines: List[str] = []

    # Chains / Agents
    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:  # type: ignore[override]
        self._lines.append("> Entering new AgentExecutor chain...")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:  # type: ignore[override]
        self._lines.append("> Finished chain.")
        try:
            # Many agents return a dict with an "output" key
            if isinstance(outputs, dict):
                out_text = outputs.get("output") or outputs.get("answer")
                if out_text:
                    self._lines.append(str(out_text))
            else:
                self._lines.append(str(outputs))
        except Exception:
            pass

    # Tools
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> None:  # type: ignore[override]
        try:
            name = serialized.get("name") or "tool"
        except Exception:
            name = "tool"
        self._lines.append(f"Invoking: `{name}` with `{input_str}`")

    def on_tool_end(self, output: str, **kwargs: Any) -> None:  # type: ignore[override]
        if output:
            self._lines.append(str(output))

    # LLMs (optional - keep minimal to avoid overly verbose traces)
    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:  # type: ignore[override]
        self._lines.append(f"LLM Error: {error}")

    def get_transcript(self) -> str:
        return "\n".join(self._lines).strip()


