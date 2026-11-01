"""LLM access for the agents: DeepSeek through its OpenAI-compatible API.

Every request and response is appended to a JSONL log, so a run can be audited
for what was sent (it must only ever be code, rules and aggregate metrics).
`FakeLLM` replays scripted responses for offline tests.
"""

from __future__ import annotations

import json
import os
import time
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-flash"


def load_dotenv(path: Path = ROOT / ".env") -> None:
    """Minimal .env reader: KEY=VALUE lines, existing environment wins."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))


class LLM:
    """chat(messages, tools) -> assistant message dict ({"content", "tool_calls"})."""

    def __init__(self, log_path: Path | None = None) -> None:
        self.log_path = log_path

    def chat(self, messages: list[dict], tools: list[dict] | None = None, json_mode: bool = False,
             agent: str = "?") -> dict:
        raise NotImplementedError

    def _log(self, role: str, messages: list[dict], reply: dict) -> None:
        if self.log_path is None:
            return
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"at": time.time(), "agent": role, "request": messages, "reply": reply}) + "\n")


class DeepSeekLLM(LLM):
    def __init__(self, model: str | None = None, log_path: Path | None = None, max_retries: int = 3) -> None:
        super().__init__(log_path)
        from openai import OpenAI

        load_dotenv()
        key = os.environ.get("DEEPSEEK_API_KEY")
        if not key:
            raise RuntimeError("DEEPSEEK_API_KEY is not set (put it in .env)")
        self.model = model or os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL)
        self.client = OpenAI(api_key=key, base_url=DEEPSEEK_BASE_URL, max_retries=max_retries, timeout=300)

    def chat(self, messages: list[dict], tools: list[dict] | None = None, json_mode: bool = False,
             agent: str = "?") -> dict:
        kwargs = {"model": self.model, "messages": messages}
        if tools:
            kwargs["tools"] = tools
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        message = self.client.chat.completions.create(**kwargs).choices[0].message
        reply = {"role": "assistant", "content": message.content or ""}
        if message.tool_calls:
            reply["tool_calls"] = [
                {"id": c.id, "type": "function", "function": {"name": c.function.name, "arguments": c.function.arguments}}
                for c in message.tool_calls
            ]
        self._log(agent, messages, reply)
        return reply


class FakeLLM(LLM):
    """Replays `script`: each item is a reply dict or a callable(messages) -> reply dict."""

    def __init__(self, script: list[dict | Callable[[list[dict]], dict]], log_path: Path | None = None) -> None:
        super().__init__(log_path)
        self.script = list(script)
        self.calls: list[list[dict]] = []

    def chat(self, messages: list[dict], tools: list[dict] | None = None, json_mode: bool = False,
             agent: str = "?") -> dict:
        self.calls.append(list(messages))
        if not self.script:
            raise RuntimeError("FakeLLM script exhausted")
        item = self.script.pop(0)
        reply = item(messages) if callable(item) else item
        reply = {"role": "assistant", "content": "", **reply}
        self._log(agent, messages, reply)
        return reply


def tool_spec(name: str, description: str, properties: dict, required: list[str]) -> dict:
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object", "properties": properties, "required": required, "additionalProperties": False},
    }}


def run_tools(llm: LLM, agent: str, system: str, user: str, tools: dict[str, tuple[dict, Callable[..., str]]],
              max_rounds: int = 12, stop_when: Callable[[], bool] | None = None) -> str:
    """Tool-calling loop. `tools` maps name -> (spec, handler(**args) -> str). Returns the final text."""
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    specs = [spec for spec, _ in tools.values()]
    for _ in range(max_rounds):
        reply = llm.chat(messages, tools=specs, agent=agent)
        messages.append(reply)
        calls = reply.get("tool_calls") or []
        if not calls:
            return reply.get("content", "")
        for call in calls:
            name = call["function"]["name"]
            try:
                args = json.loads(call["function"]["arguments"] or "{}")
                output = tools[name][1](**args) if name in tools else f"unknown tool {name!r}"
            except Exception as exc:  # noqa: BLE001 - tool errors go back to the model
                output = f"tool error: {type(exc).__name__}: {exc}"
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": output})
        if stop_when and stop_when():
            return ""
    return ""


def chat_json(llm: LLM, agent: str, system: str, user: str, retries: int = 2) -> dict:
    """One structured reply. The prompt must ask for a JSON object."""
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    for _ in range(retries + 1):
        reply = llm.chat(messages, json_mode=True, agent=agent)
        try:
            return json.loads(reply.get("content") or "")
        except json.JSONDecodeError:
            messages += [reply, {"role": "user", "content": "That was not valid JSON. Reply with one JSON object only."}]
    raise RuntimeError(f"{agent}: no valid JSON after {retries + 1} attempts")
