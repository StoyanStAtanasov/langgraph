from typing import Any, TypedDict
from uuid import UUID, uuid4
from langchain.agents import create_agent, AgentState
from dotenv import load_dotenv
from langchain_core.messages import AIMessageChunk
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph
from langchain.agents.middleware.types import (
    AgentState,
    _InputAgentState,
    _OutputAgentState,
)


load_dotenv()


class AgentConfig(TypedDict):
    model: str
    tools: list[str]
    system_prompt: str


def weather_tool(city: str) -> str:
    """Get the weather for a city."""
    return f"it's sunny and 70 degrees in {city}"


agentConfig = AgentConfig(
    model="openai:openai/gpt-oss-20b",
    tools=["weather_tool"],
    system_prompt="You are a helpful research assistant.",
)


def create_configurable_agent(
    config: AgentConfig,
) -> CompiledStateGraph[AgentState, Any, _InputAgentState, _OutputAgentState]:
    
    tools = []
    for tool_name in config["tools"]:
        match tool_name:
            case "weather_tool":
                tools.append(weather_tool)

    return create_agent(
        model=config["model"],
        tools=tools,
        system_prompt=config["system_prompt"],
        checkpointer=InMemorySaver(),
    )


async def run_agent_streaming_response(
    agent: CompiledStateGraph[AgentState, Any, _InputAgentState, _OutputAgentState],
    session_id: UUID,
    input_text: str,
) -> str:

    response = agent.astream(
        input={
            "messages": [
                {
                    "role": "user",
                    "content": input_text,
                }
            ]
        },
        stream_mode=["messages", "updates"],
        config={"configurable": {"thread_id": str(session_id)}},
    )

    async for event_type, event in response:
        if event_type == "messages":
            chunk, state = event
            if isinstance(chunk, AIMessageChunk):
                print(chunk.content, end="", flush=True)


async def main():
    agent = create_configurable_agent(agentConfig)
    session_id = uuid4()
    await run_agent_streaming_response(
        agent, session_id, "My name is John. What's the weather like in New York?"
    )
    print("\n---\n")
    await run_agent_streaming_response(agent, session_id, "What is my name?")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
