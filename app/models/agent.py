from typing import Optional

from sqlmodel import SQLModel, Field
from enum import Enum


class AgentStatus(str, Enum):
    CREATED = 'CREATED'
    CREATING = 'CREATING'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class Agent(SQLModel, table=True):
    agent_name: str = Field(index=True, primary_key=True)
    game_name: str = Field(nullable=False)
    temperature_hints: Optional[str] = Field(default=None, nullable=True)
    status: AgentStatus = Field(default=AgentStatus.CREATED)
    collection_name: Optional[str] = Field(default=None, nullable=True)
