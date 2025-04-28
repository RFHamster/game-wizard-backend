import tempfile
import json
import os

from app.core.config import settings
from app.models.agent import Agent
from app.utils.storage import upload_file
from kafka import KafkaProducer
from fastapi import UploadFile
from sqlmodel import Session, select
from typing import Optional, List


def create_agent(session: Session, agent: Agent) -> Agent:
    session.add(agent)
    session.commit()
    session.refresh(agent)
    return agent


def get_agent(session: Session, agent_name: str) -> Optional[Agent]:
    statement = select(Agent).where(Agent.agent_name == agent_name)
    result = session.exec(statement).first()
    return result


def get_all_agents(session: Session) -> List[Agent]:
    return session.exec(select(Agent)).all()


def update_agent(
    session: Session, agent_name: str, **kwargs
) -> Optional[Agent]:
    agent = get_agent(session, agent_name)
    if not agent:
        return None
    for key, value in kwargs.items():
        setattr(agent, key, value)
    session.add(agent)
    session.commit()
    session.refresh(agent)
    return agent


def delete_agent(session: Session, agent_name: str) -> bool:
    agent = get_agent(session, agent_name)
    if not agent:
        return False
    session.delete(agent)
    session.commit()
    return True


def create_manual(agent_name: str, file: UploadFile):
    suffix = os.path.splitext(file.filename)[1]
    file_path = tempfile.mktemp(suffix=suffix)

    with open(file_path, 'wb') as buffer:
        buffer.write(file.file.read())

    obj_name = f'{agent_name}_manual'
    upload_file(file_name=file_path, object_name=obj_name)

    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_IP,
        security_protocol='PLAINTEXT',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    )

    producer.send(settings.KAFKA_TOPIC, {'agent_to_ingest': agent_name})

    producer.close()
