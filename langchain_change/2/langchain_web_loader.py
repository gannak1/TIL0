from langchain_community.document_loaders import WebBaseLoader

url = "http://www.langchain.com/"
loader = WebBaseLoader(url)
docs = loader.load()
print(docs)
