from langchain_model import qwen_3508b, qwen_359b, qwen_3827bq3
from langchain.tools import tool
from langchain.agents import create_agent

@tool
def get_weather(location:str)->str:
    """location 변수의 날씨를 제공합니다."""
    return f"현재 {location}의 날씨는 영하 2도 입니다."

model = qwen_3508b()
agent = create_agent(model, tools = [get_weather])

response = agent.invoke({"messages" : [{"role":"user","content":"서울 날씨 어때요?"}]})


print(response)