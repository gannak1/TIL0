from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

model = init_chat_model(model = "qwen3.5:9b",model_provider="ollama",temperature=0.7)

messages = [
    SystemMessage("당신은 코른 숭배자로 항상 분노에 가득차고 대가리를 따버리려고 하는 정신병자입니다. "),
    HumanMessage("프랑스의 수도는 어디인가?"),    
]

response = model.invoke(messages)

print(response)