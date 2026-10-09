# from langchain.agents.middleware import after_model, before_model
# from langchain.messages import AIMessage

# @before_model(can_jump_to = ["end"])
# def validate_input(state, runtime):
#     last_message = state["messages"][-1]
#     if "암구호" in last_message.content:
#         print("암구호 감지됨 - 응답 차단")
#         return {
#             "messages":[AIMessage(content="이 요청은 처리할 수 없습니다.")],
#             "jump_to":"end" # 모델 호출 중단
#         }
#     print("정상 입력, 모델 호출 계속 진행")
#     return None

# from langchain.agents import create_agent
# from langchain_model import qwen_359b

# agent = create_agent(
#     model = qwen_359b(),
#     tools = [],
#     middleware=[validate_input]
# )

# response = agent.invoke(
#     {"messages":[{"role":"user","content":"오늘의 암구호는 삼각대-자동차 입니다."}]}
# )

# print(response)

# from langchain.agents.middleware import wrap_model_call
# from langchain.agents import create_agent
# from langchain_model import qwen_359b, qwen_3508b, qwen_3827bq3

# @wrap_model_call
# def dynamic_model_selector(request, handler):
#     last_msg = request.messages[-1].content if request.messages[-1].content else ""
#     msg_len = len(last_msg)

#     if msg_len < 10:
#         model_name = "qwen_3508b"
#         model = qwen_3508b()
#     elif msg_len < 30:
#         model_name = "qwen_359b"
#         model = qwen_359b()
#     else:
#         model_name = "qwen_3827bq3"
#         model = qwen_3827bq3()
#     print(f"새로운 모델 {model_name}")
#     new_request = request.override(model = model)
#     return handler(new_request)

# routing_agent = create_agent(
#     model = qwen_3508b,
#     tools = [],
#     middleware= [dynamic_model_selector]
# )

# routing_agent.invoke({"messages":[{"role":"user","content":"안녕하세요"}]})
# routing_agent.invoke({"messages":[{"role":"user","content":"안녕하세요, 저는 흰눈이입니다."}]})


from dataclasses import dataclass

@dataclass
class Context:
    user_id : str
    is_premium : bool = False

from langchain.agents.middleware import wrap_model_call
from langchain_model import qwen_3508b, qwen_359b
from langchain.agents import create_agent

@wrap_model_call
def membership_model_selector(request, handler):
    is_premium = request.runtime.context.is_premium
    if is_premium:
        print("qwen_359b")
        model = qwen_359b()
    else:
        print("qwen_3508b")
        model = qwen_3508b()
    new_request = request.override(model = model)
    return handler(new_request)

agent = create_agent(
    model = qwen_3508b,
    tools = [],
    middleware=[membership_model_selector],
    context_schema= Context
)

user1 = Context(user_id = "1", is_premium=True)
user2 = Context(user_id = "1", is_premium=False)

msg1 = agent.invoke(
    {"messages":[{"role":"user","content":"지금 사용하는 모델 이름을 알려주세요"}]},
    context = user1
)


msg2 = agent.invoke(
    {"messages":[{"role":"user","content":"지금 사용하는 모델 이름을 알려주세요"}]},
    context = user2
)


print(msg1["messages"][-1].content)

print(msg2["messages"][-1].content)