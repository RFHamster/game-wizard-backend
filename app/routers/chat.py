from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/chat', tags=['chat'])

class UserInput(BaseModel):
    input: str

@router.post('/{agent_name}')
async def health_check(agent_name: str, user_input: UserInput):
    return {
        "status": "ok",
        "agent": agent_name,
        "input_received": user_input.input,
        "message": f"EI EI MAEL, agente {agent_name} ativo."
    }
