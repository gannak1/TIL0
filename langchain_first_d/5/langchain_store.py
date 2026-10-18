
from langchain_community.document_loaders import PDFPlumberLoader

loader = PDFPlumberLoader("./content/ARK_INNOVATION_ETF_ARKK_HOLDINGS.pdf")
docs = loader.load()

from langchain_text_splitters import RecursiveCharacterTextSplitter
pdf_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 150,
)

recursive_docs = pdf_splitter.split_documents(docs)

from langchain_ollama import OllamaEmbeddings
from langchain_classic.embeddings import CacheBackedEmbeddings
from langchain_classic.storage import LocalFileStore

underlying_embeddings = OllamaEmbeddings(model = "qwen3-embedding:0.6b")

store = LocalFileStore("./cache/")

cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings,
    store,
    namespace = underlying_embeddings.model.replace(":","_")
)

from langchain_chroma import Chroma

# 1. DB 경로 설정
CHORMA_PATH = "./chroma_db"

# 2. Store 생성
db = Chroma.from_documents(
    documents = recursive_docs, # split 한 문서 리스트
    embedding = cached_embedder, # 임베딩 모델
    persist_directory = CHORMA_PATH, # 데이터를 저장할 폴더 경로
    collection_name = "rag_collection" # (선택) DB 내의 테이블 이름 같은 개념
)

# 사용자의 질문 정의
query = "ARK Innovation ETF의 보유 비중 상위 종목은?"

# 질문과 의미가 가장 유사한 문서 3개(k=3)를 검색
results = db.similarity_search(query, k=3)

print(len(results))
print(f"검색된 문서 내용:\n{results[0].page_content}")