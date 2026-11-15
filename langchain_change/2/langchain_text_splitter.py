from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(f"document\현진건-운수_좋은_날+B3356-개벽.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=200)
# splitted_docs = splitter.split_documents(docs)
# print(splitted_docs)

python_code = '''
def hello_world():
    print("Hello World")

#Call the Function
hello_world()
'''

splitted_docs = splitter.create_documents([python_code])
print(splitted_docs)