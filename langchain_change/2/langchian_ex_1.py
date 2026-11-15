from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader(f"document\현진건-운수_좋은_날+B3356-개벽.pdf")
splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
splitted_docs = splitter.split_documents(loader.load())

from langchain.embeddings import init_embeddings

embedding_model = init_embeddings(model = "qwen3-embedding:0.6b",provider="ollama")
embedding_docs = embedding_model.embed_documents([doc.page_content for doc in splitted_docs])
print(embedding_docs)