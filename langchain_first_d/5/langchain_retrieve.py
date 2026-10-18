from langchain_community.document_loaders import PDFPlumberLoader
loader = PDFPlumberLoader("./content\ARK_INNOVATION_ETF_ARKK_HOLDINGS.pdf")
docs = loader.load()

from langchain_split import RecursiveCharacterTextSplitter
RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 150,
)

from langchain_ollama import OllamaEmbeddings
from langchain_classic.storage import LocalFileStore
from langchain_classic.embeddings import CacheBackedEmbeddings
underlying_embeddings = OllamaEmbeddings(model = "qwen3-embedding:0.6b")
store = LocalFileStore("./cache/")

cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings,
    store,
    namespace = underlying_embeddings.model.replace(":","_")
)

from langchain_chroma import Chroma
from langchain_core.documents import Document

CHORMA_PATH = "./chroma_db"

db = Chroma(
    collection_name = "rag_collection",
    embedding_function = cached_embedder,
    persist_directory = CHORMA_PATH,
    collection_metadata = {"hnsw:space":"cosine"}
)

retriever = db.as_retriever(
    search_type = "similarity_score_threshold",
    search_kwargs = {"score_threshold":0.3}
)

# results = retriever.invoke("ARKK의 Tesla 투자 비중은?")
# print(len(results))

# print(f"검색된 문서 내용 : \n{results[0].page_content}")

# retriever = db.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={"score_threshold": 0.9}
# )
# results = retriever.invoke("ARKK의 Tesla 투자 비중은?")
# print("retrieved:", len(results))

# retriever = db.as_retriever(
#     search_type="mmr",
#     search_kwargs={
#         "k": 5,          # 최종적으로 가져올 문서 개수
#         "fetch_k": 20    # 1차로 검색할 후보 문서 개수 (이 중에서 중복을 제거해 5개를 추림)
#     }
# )

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_model import qwen_359b
from langchain.messages import HumanMessage, SystemMessage

model = qwen_359b()

# 1단계 (Retrieve): 관련 문서 검색
query = "ARKK의 Tesla 투자 비중은?"
retrieved_docs = retriever.invoke(query)

# 검색된 문서의 내용(page_content)을 하나의 텍스트로 합치기
context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

# 2단계 (Generate): 프롬프트 구성 및 LLM 호출
system_prompt = f"""당신은 ARKK 펀드 전문 어시스턴트입니다.
아래 제공된 문맥(Context)을 바탕으로 사용자의 질문에 상세히 답변하세요.
문맥에 없는 내용은 지어내지 말고 모른다고 답변하세요.

<문맥(Context)>
{context_text}
</문맥(Context)>
"""
messages = [SystemMessage(content = system_prompt), HumanMessage(content = query)]

ai_response = model.invoke(messages)
print(ai_response)