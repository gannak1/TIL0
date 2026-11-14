a = ("system","당신은 친절한 어시스턴트입니다.")
b=  ("human","{question}")
c = {"question":"거대 언어 모델은 어디서 제공하나요?"}

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import chain
from langchain.chat_models import init_chat_model

model = init_chat_model(model = "qwen3.5:9b",model_provider="ollama")

prompts = ChatPromptTemplate.from_messages([
    a,b
])

@chain
def chatbot(values):
    template = prompts.invoke(values)
    return model.invoke(template)


print('시작')
print(chatbot.invoke(c))

