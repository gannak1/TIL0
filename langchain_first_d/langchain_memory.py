from langchain_model import qwen_359b
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from time import time

c = time()
model = qwen_359b()
agent = create_agent(model = model, checkpointer=InMemorySaver())

cfg = {
    "configurable" : {"thread_id" : "1"}
}

response = agent.invoke(
    {"messages": [{"role":"user","content":"안녕하세요 저는 최강의 강아지 흰눈이입니다."}]},
    cfg
)

print("[에이전트 답변]: ", response["messages"][-1].content)

response = agent.invoke(
    {"messages": [{"role":"user","content":"내 이름이 뭐라고?"}]},
    cfg
)

print("[에이전트 답변]:", response["messages"][-1].content)


response = agent.invoke(
    {"messages":{"role":"user","content":"지금까지 나눈 이야기를 알려줘"}},
    {"configurable":{"thread_id":"1"}}
    )

for i, msg in enumerate(response["messages"], start = 1):
    print(f"--- Message {i} ({msg.type}) ---")
    print(msg.content)
    print()

print("------------------------------걸린 시간-------------------------------")
print(f"{time() - c}초")