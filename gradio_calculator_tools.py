import json

import gradio as gr
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool

from chat import create_llm

SYSTEM_ROLE = (
    "You are a calculator assistant. "
    "When the user asks for any arithmetic in natural language, "
    "you must call the addition, minus, multiply, or division tools. "
    "Do not calculate in your head. Use the tools, then give a short final answer."
)


@tool
def addition(a: float, b: float) -> float:
    """Add two numbers together. Use for plus, sum, or addition."""
    return a + b


@tool
def minus(a: float, b: float) -> float:
    """Subtract b from a. Use for minus, subtract, or difference."""
    return a - b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers. Use for times, product, or multiplication."""
    return a * b


@tool
def division(a: float, b: float) -> float:
    """Divide a by b. Use for divide, quotient, or division. Do not divide by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


TOOLS = [addition, minus, multiply, division]
TOOL_MAP = {t.name: t for t in TOOLS}

_llm_with_tools = None


def get_llm_with_tools():
    global _llm_with_tools
    if _llm_with_tools is None:
        _llm_with_tools = create_llm().bind_tools(TOOLS)
    return _llm_with_tools


def _format_call(name: str, args: dict, result: str) -> str:
    return f"{name}({json.dumps(args)}) -> {result}"


def run_with_tools(user_text: str, max_rounds: int = 5) -> tuple[str, str]:
    user_text = (user_text or "").strip()
    if not user_text:
        return "Please enter a question.", "No tools called."

    messages = [
        SystemMessage(content=SYSTEM_ROLE),
        HumanMessage(content=user_text),
    ]
    llm_with_tools = get_llm_with_tools()
    traces: list[str] = []

    for _ in range(max_rounds):
        ai = llm_with_tools.invoke(messages)
        messages.append(ai)
        if not getattr(ai, "tool_calls", None):
            answer = ai.content or ""
            log = "\n".join(traces) if traces else "No tools called."
            return answer, log

        for call in ai.tool_calls:
            name = call["name"]
            args = call.get("args") or {}
            tool = TOOL_MAP.get(name)
            if tool is None:
                result = f"Unknown tool: {name}"
            else:
                try:
                    result = tool.invoke(args)
                except Exception as exc:
                    result = str(exc)
            traces.append(_format_call(name, args, result))
            messages.append(
                ToolMessage(content=str(result), tool_call_id=call["id"])
            )

    return "Stopped after too many tool rounds.", "\n".join(traces)


def answer_question(question: str) -> tuple[str, str]:
    return run_with_tools(question)


demo = gr.Interface(
    fn=answer_question,
    inputs=gr.Textbox(
        label="Ask in natural language",
        placeholder="What is twelve plus thirty?",
        lines=3,
    ),
    outputs=[
        gr.Textbox(label="Model answer", lines=6),
        gr.Textbox(label="Tools the model called", lines=8),
    ],
    title="Calculator Tools (bind_tools)",
    description=(
        "The model is bound to four tools with bind_tools: addition, minus, "
        "multiply, and division. Ask in everyday language and the model should "
        "call those tools instead of doing the math itself."
    ),
    examples=[
        ["What is twelve plus thirty?"],
        ["Please subtract 9 from 40."],
        ["Multiply 6 by 7 for me."],
        ["Divide one hundred by four."],
    ],
    flagging_mode="never",
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7867, share=True)
