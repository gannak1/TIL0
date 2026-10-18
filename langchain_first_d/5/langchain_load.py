# from langchain_community.document_loaders import PDFPlumberLoader

# file_path = "./content/ARK_INNOVATION_ETF_ARKK_HOLDINGS.pdf"
# loader = PDFPlumberLoader(file_path)
# docs = loader.load()
# docs[0]
# len(docs)


# from langchain_community.document_loaders import PyMuPDFLoader
# import pprint

# file_path = "./content/ARK_INNOVATION_ETF_ARKK_HOLDINGS.pdf"
# loader = PyMuPDFLoader(file_path)
# docs_pymupdf = loader.load()

# pprint.pp(docs_pymupdf[0].metadata)

# # 웹페이지 데이터를 로드하는 WebBaseLoader 예시 (참고용)
# from langchain_community.document_loaders import WebBaseLoader

# loader = WebBaseLoader("https://example.com")
# web_docs = loader.load()


# from langchain_hwp_hwpx import HwpHwpxLoader

# file_path = "/content/20251128_국민연금_2025년_9월_말_기금_운용수익률.hwp"
# loader = HwpHwpxLoader(file_path, mode="elements")
# docs_hwp = loader.load()