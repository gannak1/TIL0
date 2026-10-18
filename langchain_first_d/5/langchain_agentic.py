import sys
from pathlib import Path

# 부모 Path 추가
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# from langchain_model import qwen_359b

# model = qwen_359b()

# response = model.invoke("ARKK 펀드의 Tesla 투자 비중이 어떻게 돼?")
# print(response.content)

# 학습 데이터의 한계(Cut off) 때문에 최신 수치 확인이 어럽다고 회피
# 근거 없이 그럴싸한 가짜 숫자를 만들어냄 (할루시네이션)

from langchain_ollama import OllamaEmbeddings
from langchain_classic.storage import LocalFileStore
from langchain_classic.embeddings import CacheBackedEmbeddings
underlying_embeddings = OllamaEmbeddings(model = "qwen3-embedding:0.6b")
store = LocalFileStore("./cache/")
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings,
    store,
    namespace = underlying_embeddings.model.replace(":","_"),
)

from langchain_community.document_loaders import PDFPlumberLoader
loader = PDFPlumberLoader("./content\ARK_INNOVATION_ETF_ARKK_HOLDINGS.pdf")
docs = loader.load()

from langchain_split import RecursiveCharacterTextSplitter
pdf_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 150,
)
recursive_pdf = pdf_splitter.split_documents(docs)

from langchain_chroma import Chroma
from langchain_core.documents import Document

CHROMA_PATH = "./chroma_db"

db = Chroma(
    collection_name = "rag_collection",
    embedding_function = cached_embedder,
    persist_directory = CHROMA_PATH,
    collection_metadata = {"hnsw:space":"cosine"}
)

retriever = db.as_retriever(
    search_type = "similarity_score_threshold",
    search_kwargs = {"score_threshold":0.3}
)

from langchain.tools import tool

@tool
def search_portfolio(query:str)->str:
    """
    ARKK ETF의 포트폴리오 정보를 검색할 때 사용합니다.
    특정 기업의 보유 비중, 주식 수, 가치 등을 찾을 때 이 도구를 호출하세요.
    """
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])
from typing import Literal
import math

@tool
def calculate_math(a:float, b:float, operation:Literal["add","subtract",'multiply','divide'])->float:
    """두 유한한 수의 사칙 연산, 예: a=12.26, b=2, operation='multiply."""
    if not math.isfinite(a) or not math.isfinite(b):
        raise ValueError("유한한 수만 입력하세요.")
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("0으로 나눌 수 없습니다.")
        return a / b
    raise ValueError("지원하지 않는 연산입니다.")

from langchain.agents import create_agent
from langchain_model import qwen_359b

agent = create_agent(
    model = qwen_359b(),
    tools = [search_portfolio,calculate_math]
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "ARKK 펀드의 Tesla 투자 비중을 찾고, 그 비중의 2배가 얼마인지 계산해 줘."}]},
)

print(response['messages'][-1].content)

# BM25 검색
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

# 텍스트 리스트 준비
retriever = BM25Retriever.from_texts(["foo", "bar", "world", "hello", "foo bar"])

# 'foo'와 가장 연관성 높은 문서 검색
result = retriever.invoke("foo")
print(result)

from kiwipiepy import Kiwi

# 1. Kiwi 형태소 분석기 준비
kiwi = Kiwi()

# 2. 전처리 함수 정의 (각 형태소의 표면형 추출 (조사·어미 포함))
def korean_tokenizer(text):
    # kiwi.tokenize()는 토큰 정보를 반환하므로, 거기서 단어 형태(form)만 추출
    return [token.form for token in kiwi.tokenize(text)]

print(korean_tokenizer("테슬라는 전기차를 만듭니다."))