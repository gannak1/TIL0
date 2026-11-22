from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitter import RecursiveCharacterTextSplitter

embedding_model = init_embeddings(model = "qwen3-embedding:0.6b",provider = "ollama")
llm = init_chat_model(model = "qwen3.5:9b",model_provider="ollama",temperature=0)

docs = PyPDFLoader("document\현진건-운수_좋은_날+B3356-개벽.pdf").load()
splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
chunks = splitter.split_documents(docs)

from langchain_postgres.vectorstores import PGVector
from langchain_classic.indexes import index, SQLRecordManager
import uuid

connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"
vectorstore = PGVector(
    embeddings = embedding_model,
    connection=connection,
    collection_name="summarize",
    use_jsonb=True
)

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt_text = "다음 문서의 요약을 생성하세요:\n\n{doc}"

prompt = ChatPromptTemplate.from_template(prompt_text)
summarize_chain = {
    'doc': lambda x:x.page_content } | prompt | llm | StrOutputParser()

summarize= summarize_chain.batch(chunks, {'max_concurrency':5})

from langgraph.store.memory import InMemoryStore
from langchain_classic.retrievers.multi_vector import MultiVectorRetriever

store = InMemoryStore()
id_key = 'doc_id'

retriever = MultiVectorRetriever(
    vectorstore = vectorstore,
    docstore=store,
    id_key = id_key
)

# 문서와 동일한 길이가 필요하므로 summaries에서 chunks로 변경
doc_ids = [str(uuid.uuid4()) for _ in chunks]

# 각 요약은 doc_id를 통해 원본 문서와 연결
summary_docs = [
    Document(page_content = s, metadata={id_key:doc_ids[i]})
             for i,s in enumerate(summarize)
]

# 유사도 검색을 위해 벡터 저장소에 문서 요약을 추가
retriever.vectorstore.add_documents(summary_docs)

# doc_ids를 통해 요약과 연결된 원본 문서를 문서 저장소에 저장
# 이를 통해 먼저 요약을 효율적으로 검색한 다음 필요할 때 전체문서를 가져옴
retriever.docstore.mset(list(zip(doc_ids, chunks)))

# 벡터 저장소가 요약을 검색
sub_docs = retriever.vectorstore.similarity_search(
    'chapter on philosophy', k=2
)

print('sub docs: ', sub_docs[0].page_content)

print('length of sub docs:\n', len(sub_docs[0].page_content))
# retriever는 더 큰 원본 문서 청크를 반환
retrieved_docs = retriever.invoke("chapter on philosophy")

print("length of retrieved docs: ", len(retrieved_docs[0].page_content))