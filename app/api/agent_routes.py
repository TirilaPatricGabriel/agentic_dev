from fastapi import APIRouter
from pydantic import BaseModel
from typing import AsyncGenerator
from fastapi.responses import StreamingResponse
import json

from app.agents.coding_agent.agent import CodingAgent

router = APIRouter(prefix="/agent", tags=["agent"])
coding_agent = CodingAgent()

class AgentRequest(BaseModel):
    query: str

class AgentResponse(BaseModel):
    response: str

@router.post("/invoke", response_model=AgentResponse)
async def invoke_agent(request: AgentRequest):
    result = coding_agent.invoke(request.query)
    return AgentResponse(response=str(result))

@router.post("/stream")
async def stream_agent(request: AgentRequest):
    async def event_generator() -> AsyncGenerator[str, None]:
        for message in coding_agent.stream(request.query):
            sender = message.type.upper()
            content = message.content

            if not content and hasattr(message, 'tool_calls') and message.tool_calls:
                tool_names = [tc['name'] for tc in message.tool_calls]
                data = {
                    "sender": sender,
                    "type": "tool_call",
                    "tools": tool_names
                }
            else:
                data = {
                    "sender": sender,
                    "type": "message",
                    "content": content
                }

            yield f"data: {json.dumps(data)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
