from typing import Annotated, List

from app.core.db import get_session
from app.models.agent import Agent
from app.utils.crud import (
    create_agent,
    get_agent,
    update_agent,
    delete_agent,
    get_all_agents,
    create_manual,
)
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session


router = APIRouter(prefix='/agent', tags=['agent'])


@router.get('/', response_model=List[Agent])
def read_all_agents(session: Session = Depends(get_session)):
    agent = get_all_agents(session)
    if not agent:
        raise HTTPException(status_code=404, detail='Agent not found')
    return agent


@router.get('/{agent_name}', response_model=Agent)
def read_agent(agent_name: str, session: Session = Depends(get_session)):
    agent = get_agent(session, agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail='Agent not found')
    return agent


@router.post('/', response_model=Agent)
def create_agent_route(
    agent_name: Annotated[str, Form()],
    game_name: Annotated[str, Form()],
    temperature_hints: Annotated[str, Form()],
    manual_file: Annotated[UploadFile, File()],
    session: Session = Depends(get_session),
):
    agent_in = Agent(
        agent_name=agent_name,
        game_name=game_name,
        temperature_hints=temperature_hints,
    )
    agent = create_agent(session, agent_in)
    manual = create_manual(agent.agent_name, manual_file)
    return agent


@router.put('/{agent_name}', response_model=Agent)
def update_agent_route(
    agent_name: str,
    agent_update: Agent,
    session: Session = Depends(get_session),
):
    agent = update_agent(
        session, agent_name, **agent_update.dict(exclude_unset=True)
    )
    if not agent:
        raise HTTPException(status_code=404, detail='Agent not found')
    return agent


@router.delete('/{agent_name}', status_code=204)
def delete_agent_route(
    agent_name: str, session: Session = Depends(get_session)
):
    deleted = delete_agent(session, agent_name)
    if not deleted:
        raise HTTPException(status_code=404, detail='Agent not found')
    return
