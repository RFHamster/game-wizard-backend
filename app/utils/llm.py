from langchain_core.prompts import PromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers.string import StrOutputParser

from app.core.config import settings

template = """
Você é o {agent_name}, um assistente especializado em {game_name}.
Sua função é ajudar os jogadores com suas dúvidas, explicando sua dúvida.


Aqui estão pedaços recuperados do manual do jogo, eles serão usadas como contexto para responder perguntas, mas também utilize seu conhecimento de especialista.

Contexto disponível:
{manual_chunks}

Instruções de tom e configuração para sua resposta:
{style_and_config}

Com base no contexto acima, responda a pergunta do usuário da forma mais clara e objetiva possível.

Pergunta: {question}
Resposta:
"""


def load_nvidia_chat_model(model_name: str) -> ChatNVIDIA:
    return ChatNVIDIA(
        model=model_name,
        api_key=settings.NVIDIA_NIM_API_KEY,
        top_p=0.7,
        max_tokens=21000,
        temperature=0.2,
        context_length=120000,
    )


def init_llm_model(model_name: str):
    return load_nvidia_chat_model(model_name)


def get_db_agent():
    llm = init_llm_model(settings.LLM_LLAMA_33_70B_INSTRUCT)
    return (
        PromptTemplate(
            input_variables=[
                'agent_name',
                'game_name',
                'manual_chunks',
                'style_and_config',
                'question',
            ],
            template=template,
        )
        | llm
        | StrOutputParser()
    )
