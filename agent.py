from dataclasses import dataclass
import selectors
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
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from starlette.responses import StreamingResponse


load_dotenv()


@dataclass
class Context:
    city: str


class AgentConfig(TypedDict):
    model: str
    tools: list[str]
    system_prompt: str
    context: Context | None


@tool
def weather_tool(runtime: ToolRuntime[Context], city: str | None) -> str:
    """Get the weather for a city. If no city is provided, use the city from context."""
    city = city or runtime.context.city
    return f"it's sunny and 70 degrees in {city}"


agentConfig = AgentConfig(
    model="openai:openai/gpt-oss-20b",
    tools=["weather_tool"],
    system_prompt="You are a helpful research assistant.",
    context=Context(city="New York"),
)


async def create_configurable_agent(
    config: AgentConfig,
    postgresCheckpointer: AsyncPostgresSaver,
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
        # checkpointer=InMemorySaver(),
        checkpointer=postgresCheckpointer,
        context_schema=Context,
    )


async def run_agent_streaming_response(
    agent: CompiledStateGraph[AgentState, Any, _InputAgentState, _OutputAgentState],
    session_id: UUID,
    input_text: str,
    context: Context | None = None,
):

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
        context=context,
    )

    async for event_type, event in response:
        if event_type == "messages":
            chunk, state = event
            if isinstance(chunk, AIMessageChunk):
                # print(chunk.content, end="", flush=True)
                yield chunk.content


async def initialize_resources():
    # e.g., connect to DB, preload cache
    print("Initializing resources...")

    global postgresCheckpointer
    postgresCheckpointer = AsyncPostgresSaver.from_conn_string(
        "postgresql://postgres:postgres@localhost/postgres"
    )


async def cleanup_resources():
    # e.g., close DB connections
    print("Cleaning up resources...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("🚀 Server is starting up...")
    await initialize_resources()

    yield  # App runs here

    # Shutdown logic
    print("🛑 Server is shutting down...")
    await cleanup_resources()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root(input: str = "Hello World", session_id: UUID | None = None):

    async with postgresCheckpointer:

        if session_id is None:
            session_id = uuid4()

        agent = await create_configurable_agent(agentConfig, postgresCheckpointer)

        async def stream():
            async for chunk in run_agent_streaming_response(
                agent, session_id, input, context=agentConfig["context"]
            ):
                # Ensure we yield strings (StreamingResponse accepts str or bytes)
                yield chunk

        return StreamingResponse(stream(), media_type="text/plain")


if __name__ == "__main__":

    uvicorn.run(app, host="localhost", port=8000)
