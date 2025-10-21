from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.agents.langgraph_agent import LangGraphAgent

router = APIRouter()
agent = LangGraphAgent()


class ChatMessage(BaseModel):
    message: str


@router.post("/chat")
async def chat(message: ChatMessage):
    # Basic validation: message must not be empty
    if not message.message or not message.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    try:
        response = agent.process_message(message.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))