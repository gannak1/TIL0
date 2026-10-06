from dataclasses import dataclass
from langchain_model import qwen_359b, qwen_3508b, qwen_3827bq3


@dataclass
class Context:
    user_name:str

from langchain.agents.middleware import before_model

@before_model
def log_before_model(state, runtime):
    print(f"(step1)before_model_state : \n{state}")
    print(f"(step2)before_model_runtime : \n{runtime}")
    print(f"(step3)사용자 이름 : {runtime.context.user_name}")
    return None

from langchain.agents import create_agent
from langchain_model import qwen_359b

# agent = create_agent(
#     model = qwen_359b(),
#     tools = [],
#     middleware = [log_before_model],
#     context_schema= Context,
# )

# response = agent.invoke({
#     "messages":[{
#         "role":"user",
#         "content":"제 이름이 뭐죠"
#     }],
# },
# context=Context(user_name="Jay"))

# print(response)

from langchain.agents.middleware import wrap_model_call, wrap_tool_call

@wrap_model_call
def dynamic_model_selector(request, handler):
    # 최근 사용자의 입력 메세지 추출
    last_msg = request.messages[-1].content if request.messages else ""
    msg_len = len(last_msg)

    # 길이에 따라 모델 선택
    if msg_len < 10:
        model = qwen_3508b()
    elif msg_len < 30:
        model = qwen_359b()
    else:
        model = qwen_3827bq3()

    new_request = request.override(model = model)

    return handler(new_request)

from typing import Callable
from langchain.agents.middleware import ModelRequest, ModelResponse
from langchain.messages import HumanMessage, SystemMessage


@wrap_model_call
def inject_user_name(request:ModelRequest, handler:Callable[[ModelRequest],ModelResponse]) -> ModelResponse:
    print(f"request: \n(request)")

    # 1. request 보따리 안의 책상(runtime)에서 신붅븡 정보 추출
    user_name = request.runtime.context.user_name

    if user_name:
        system_message = f"사용자의 이름은 {user_name}입니다."
        # 2. request.override()를 사용해 시스템 프롬프트 덮어쓰기 (모델에게 직접 떠먹여주기)
        new_request = request.override(system_message= system_message)

    # 3. 조작된 request를 handler를 통해 모델로 전송
    return handler(new_request)

agent = create_agent(
    model = qwen_359b(),
    tools = [],
    middleware = [inject_user_name],
    context_schema= Context,
)

response = agent.invoke({
    "messages":[{
        "role":"user",
        "content":"제 이름이 뭐죠"
    }],
},
context=Context(user_name="Jay"))

print(response)