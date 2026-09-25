from langchain_model import qwen_359b
from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolEmulator, TodoListMiddleware, HumanInTheLoopMiddleware, PIIMiddleware
from langchain.tools import tool
from typing import Dict, List

@tool
def send_email_tool(to: str, subject: str, body: str) -> str:
    """지정한 주소로 이메일을 보내는 도구(프로토타입)."""
    return f"Email sent. to={to}, subject={subject}"

@tool
def read_email_tool(limit: int = 3) -> List[Dict[str, str]]:
    """최근 받은 이메일을 조회하는 도구(프로토타입)."""
    return [{"from": "hr@example.com", "subject": "정책 안내", "body": "..."}][:limit]

### LLMEmulator 설정
agent = create_agent(model = qwen_359b(), tools = [send_email_tool,read_email_tool], middleware = [LLMToolEmulator(model = qwen_359b())], system_prompt="최근에 메일 하나가 왔는데 업무 관련 메일이야.")

# response = agent.invoke(
#     {"messages": [{"role": "user", "content": "최근 온 메일 확인하고 알아서 답장해줘."}]}
# )

# print(response["messages"][-1].content)

### TodoList 설정
agent = create_agent(model = qwen_359b(), tools = [send_email_tool, read_email_tool], middleware = [LLMToolEmulator(model=qwen_359b()), TodoListMiddleware()], system_prompt="최근에 메일 하나가 왔는데 업무 관련 메일이야")

# result = agent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "온 메일 다 확인한 뒤 요약해 보고해. 그 다음 답장 작성해 회신 보내줘. 마지막으로 어떻게 보냈는지 보고해.",
#             }
#         ]
#     }
# )
# print(result["messages"][-1].content)

### Human-in-the-loop 설정
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()

agent = create_agent(model = qwen_359b(), tools = [send_email_tool, read_email_tool], middleware = [LLMToolEmulator(model = qwen_359b()),HumanInTheLoopMiddleware(
    interrupt_on = {
                # 이메일 전송은 부작용이 크므로 승인/수정/거절 옵션을 활성화
                "send_email_tool": {"allowed_decisions": ["approve", "edit", "reject"]},
                # 이메일 읽기는 단순 조회이므로 중단 없이 바로 실행 허용
                "read_email_tool":False,
    }
)],system_prompt="최근에 메일 하나가 왔는데 업무 관련 메일이야")

# cfg = {"configurable":{"thread_id":"1"}}

# response = agent.invoke(
#     {"messages":[{"role":"user","content":"무슨 메일이 왔는지 확인해줘"}],},
#      cfg
# )
# print(response["messages"][-1].content)

# # 민감한 도구(메일 발송) 호출 테스트
# prompt = "교수님한테 내일 찾아뵙겠다는 메일 작성해서 보내줘."

# response = agent.invoke(
#     {"messages": [{"role": "user", "content": prompt}]},
#     {"configurable": {"thread_id": "HIL-a"}}
# )
# print(response["messages"][-1].content)

### PII Detection 설정
@tool
def save_customer_feedback(feedback:str)->str:
    """
        최근에 받은 피드백을 DB에 저장하는 도구(프로토 타입)
    """    
    return "적용 완료"

agent = create_agent(model = qwen_359b(), tools = [save_customer_feedback], middleware = [LLMToolEmulator(model=qwen_359b()),PIIMiddleware(pii_type="email",strategy="redact",apply_to_input=True), PIIMiddleware(pii_type="credit_card",strategy="mask",apply_to_input=True)])

prompt = "안녕하세요. 이메일은 user123@example.com 입니다. 제 카드번호는 1234123443214321 입니다."
response = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

# 에이전트가 실제로 넘겨받은(마스킹된) 메시지 확인
print(response["messages"][0].content)