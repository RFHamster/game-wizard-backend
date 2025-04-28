from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from app.core.db import get_session
from app.utils.crud import get_agent
from app.utils.llm import get_db_agent
from app.utils.qdrant import search_in_qdrant

router = APIRouter(prefix='/chat', tags=['chat'])


class UserInput(BaseModel):
    input: str


@router.post('/{agent_name}')
async def chat_agent(
    agent_name: str,
    user_input: UserInput,
    session: Session = Depends(get_session),
):
    llm_agent = get_db_agent()
    user_question = user_input.input
    agent = get_agent(session=session, agent_name=agent_name)
    return {
        'status': 'ok',
        'agent': agent.agent_name,
        'input_received': user_question,
        'message': llm_agent.invoke(
            {
                'agent_name': agent_name,
                'game_name': agent.game_name,
                'manual_chunks': search_in_qdrant(
                    query_text=user_question,
                    collection_name=agent.collection_name,
                ),
                'style_and_config': agent.temperature_hints,
                'question': user_question,
            }
        ),
    }
