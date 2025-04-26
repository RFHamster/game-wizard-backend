from typing import Optional

from sqlmodel import SQLModel, Field
from enum import Enum


class ManualStatus(str, Enum):
    CREATED = 'CREATED'
    PROCESSING = 'PROCESSING'
    PROCESSED = 'PROCESSED'
    ERRORED = 'ERRORED'


class Manual(SQLModel, table=True):
    manual_name: str = Field(primary_key=True)
    agent_name: str = Field(index=True)
    bucket_url: Optional[str] = Field(nullable=True)
    collection_name: Optional[str] = Field(default=None, nullable=True)
    status: ManualStatus = Field(default=ManualStatus.CREATED)
