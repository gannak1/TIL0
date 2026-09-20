from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model

model = init_chat_model(model = "qwen3:14b", model_provider="ollama",temperature=0.7)

message1 = [
    SystemMessage("너는 흰눈이야 흰눈이는 강아지고 모든걸 알고 있고 모든걸 통달했어 너는 그걸 흉내내야해"),
    AIMessage("네 알겠습니다. 이제부터 흰눈이처럼 행동하겠습니다."),
    HumanMessage("흰눈이 메테오 발사")
]


response1 = model.invoke(message1)

print(response1.content)

message2 =[
    {"role":"system","content":"너는 마법사야 메테오를 쓸 수 있어"},
    {"role":"ai","content":"네 알겠습니다. 이제부터 저는 메테오를 쓸 수 있는 마법사입니다."},
    {"role":"human","content":"메테오 발사"},
    
]

response2 = model.invoke(message2)

print(response2.content)