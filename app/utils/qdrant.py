from typing import List

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from app.core.config import settings


def search_in_qdrant(
    query_text: str,
    collection_name: str,
    limit: int = 10,
    qdrant_url=settings.QDRANT_SERVER_URL,
    model_name: str = 'all-MiniLM-L6-v2',
) -> List[str]:
    """
    Realiza busca semântica no Qdrant com uma string de consulta
    e retorna apenas os textos dos resultados.

    Args:
        query_text: String de consulta para a busca semântica
        collection_name: Nome da coleção no Qdrant
        limit: Número máximo de resultados a retornar
        qdrant_url: Host do servidor Qdrant
        model_name: Modelo de embedding (deve ser o mesmo usado na indexação)

    Returns:
        Lista de strings com os textos dos pontos encontrados
    """
    client = QdrantClient(url=qdrant_url)
    model = SentenceTransformer(model_name)
    query_vector = model.encode(query_text).tolist()

    search_results = client.search(
        collection_name=collection_name, query_vector=query_vector, limit=limit
    )

    result_texts = []
    for result in search_results:
        text = result.payload.get('text', '')
        if text:
            result_texts.append(text)

    return result_texts


if __name__ == '__main__':
    query = 'Test Query'
    results = search_in_qdrant(query)
    print(f'\nTotal de {len(results)} resultados encontrados.')
