from langchain_classic.indexes import SQLRecordManager, index
from langchain_postgres.vectorstores import PGVector
from langchain.embeddings import init_embeddings
from langchain_core.documents import Document

connection = "postresql+psycopg://langchain:langchain@localhost:6024/langchain"
collection_name = 'my_docs'

embedding_model = init_embeddings(model = "qwen3:embeddings0.6b",provider= "ollama")
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

record_manager.create_schema()

