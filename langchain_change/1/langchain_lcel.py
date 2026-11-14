from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

a = ("system","당신은 친절한 어시스턴트입니다.")
b=  ("human","{question}")
c = {"question":"거대 언어 모델은 어디서 제공하나요?"}

model = init_chat_model(model = "qwen3.5:9b",model_provider="ollama")
template = ChatPromptTemplate.from_messages([
    a,
    b
])

chatbot = template | model

# response = chatbot.invoke(c)

# print(response)

for prompt in chatbot.stream(c):
    print(prompt.content,end = "")