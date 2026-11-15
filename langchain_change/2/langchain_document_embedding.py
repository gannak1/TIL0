from langchain.embeddings import init_embeddings

model = init_embeddings(model = "qwen3-embedding:0.6b",provider="ollama")
embeddings = model.embed_documents([
    'Hi there!',
    'Oh, Hello',
    'What\'s your name?',
    'My friends call me World',
    'Hello World!',
])

print(embeddings)