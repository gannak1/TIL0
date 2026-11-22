from langchain_classic.indexes import SQLRecordManager, index
from langchain_postgres.vectorstores import PGVector
from langchain.embeddings import init_embeddings
from langchain_core.documents import Document

connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"
collection_name = 'my_docs'

embedding_model = init_embeddings(model = "qwen3-embedding:0.6b",provider= "ollama")
namespace = "my_docs_namespace"

vectorstore = PGVector(
    embeddings = embedding_model,
    collection_name = collection_name,
    connection = connection,
    use_jsonb=True,
)

record_manager = SQLRecordManager(
    namespace = namespace,
    db_url = connection
)

# 스키마 없으면 생성
record_manager.create_schema()

# 문서 생성

docs = [
    Document(page_content = 'there are cats in the pond', metadata = {
        'id':1, 'source':'cats.txt'
    }
    ),
    Document(page_content = 'ducks are also found in the pond', metadata = {
        'id': 2, 'source':'ducks.txt'
    }
    )
    ]

# 문서 인덱싱 1회차
index_1 = index(
    docs,
    record_manager,
    vectorstore,
    cleanup = 'incremental',
    source_id_key = 'source'
)

print('인덱싱 1회차: ', index_1)

# 문서 인덱싱 2회차, 중복문서 생성 안도미
index_2 = index(
    docs,
    record_manager,
    vectorstore,
    cleanup = 'incremental',
    source_id_key = 'source'
)

print('인덱싱 2회차: ', index_2)

# 문서를 수정하면 새 버전을 저장하고, 출저가 같은 기존 문서는 삭제

docs[0].page_content = 'i just modified this document!'

index_3 = index(
    docs,
    record_manager,
    vectorstore,
    cleanup = 'incremental',
    source_id_key = 'source'
)

print('인덱싱 3회차: ', index_3)