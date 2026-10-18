# from langchain_ollama import OllamaEmbeddings

# # 임베딩 모델 생성
# embeddings = OllamaEmbeddings(model = "qwen3-embedding:0.6b")

# # 텍스트 임베딩 수행
# query_result = embeddings.embed_query("인공지능")

# print(f"벡터의 길이(차원 수): {len(query_result)}")
# print(f"변환된 벡터의 앞부분 5개 값: {query_result[:5]}")

from langchain_ollama import OllamaEmbeddings
from langchain_classic.embeddings import CacheBackedEmbeddings
from langchain_classic.storage import LocalFileStore

underlying_embeddings = OllamaEmbeddings(model = "qwen3-embedding:0.6b")

store = LocalFileStore("./cache/")

cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings,
    store,
    namespace = underlying_embeddings.model
)