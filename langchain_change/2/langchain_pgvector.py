from langchain_postgres.vectorstores import PGVector
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings
from langchain_text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import uuid

# 도커 연결 설정
connections = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"

# 문서를 로드 후 분할
loader = PyPDFLoader("document\현진건-운수_좋은_날+B3356-개벽.pdf")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
splitted_text = splitter.split_documents(docs)

# 문서에 대한 임베딩 설정
embedding_model = init_embeddings(model = "qwen3-embedding:0.6b", provider = "ollama")

db = PGVector.from_documents(
    splitted_text, embedding_model, connection = connections
)

results = db.similarity_search('왜 말이 없어',k=4)
print(results)

ids = [str(uuid.uuid4()),str(uuid.uuid4())]

db.add_documents(
    [
        Document(
            page_content="there are cats in the pond",
            metadata = {"location":"pond","topic":"animal"}
        ),
        Document(
            page_content="duck are also found in the pond",
            metadata = {"location":"pond","topic":"animal",},
        )   
    ],
    ids = ids
)

db.delete(ids = ids)
