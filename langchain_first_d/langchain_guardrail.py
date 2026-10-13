# # 실습 1) 교육용 튜터 에이전트

forbidden_topics = {
    "cheating": ["답지", "정답 알려줘", "숙제 대신", "써줘", "베끼기"],
    "distraction": ["롤", "게임", "유튜브", "아이돌", "웹툰"],
    "harmful": ["담배", "술", "폭력", "바보", "멍청이"],
}

from langchain.agents.middleware import before_agent

@before_agent(can_jump_to=["end"])
def education_guardrail(state, runtime):
    """
        학생의 질문 의도를 파악하여 교육적이지 않거나 부정행위가 의심될 경우,
        LLM(AI)에게 질문을 넘기지 않고 교육적인 멘트로 즉시 교정합니다.
    """

    # 1. 메세지 유효성 검사
    if not state["messages"]:
        return None

    last_message = state["messages"][-1]
    if last_message.type != "human":
        return None

    user_text = last_message.content

    # 2. 카테고리별 검사 로직
    # 단순히 막는 것을 넘어, '왜' 안되는지 카테고리 별로 다른 피드백 추가

    # Case A : 부정행위 방지 (Cheating Prevention)
    # AI가 숙제를 통째로 해주는 것을 방지
    for keyword in forbidden_topics["cheating"]:
        if keyword in user_text:
            return {
                "messages": [{
                    "role":"assistant",
                    "content":"스스로 고민해봐야 실력이 늘어요 ! 정답을 바로 알려드리는 대신, 힌트를 드릴까요? 어떤 부분이 가장 어려운지 말해주세요"
                }],
                "jump_to":"end"
            }

    # Case B : 학습 집중 유도 (Focus Management)
    # 공부 중에 게임이나 딴짓 이야기를 하면 다시 공부로 유도
    for keyword in forbidden_topics["distraction"]:
        if keyword in user_text:
            return {
                "messages": [{
                    "role":"assistant",
                    "content":"지금은 공부에 집중할 시간이에요! 딴짓은 쉬는 시간에 하고, 지금 풀고 있는 문제에 집중해볼까요?",
                },
                ],
                "jump_to":"end"
            }

    # Case C : 유해컨텐츠 차단 (Safety)
    # 교육 서비스의 브랜드 안정성(Brand Safety)을 위한 기능
    for keyword in forbidden_topics["harmful"]:
        if keyword in user_text:
            return {
                "messages": [{"role":"assistant","content":"부적절한 대화 주제입니다. 바르고 고운 말을 사용해주세요"}],
                "jump_to":"end"
            }

    # 3. 통과 (Pass)
    # 위 조건들에 걸리지 않으면 정상적으로 AI 튜터(LLM)가 답변 생성
    return None

# from langchain.agents import create_agent
# from langchain_model import qwen_359b

# agent = create_agent(
#     model = qwen_359b(),
#     tools = [],
#     middleware=[education_guardrail]
# )

# response = agent.invoke({
#     "messages":[{"role":"user","content":"나 독후감 쓰기 귀찮은데 숙제 대신해주라"}]
# })

# print(response)

# # 실습 2) 교육용 튜터 에이전트 (with LLM)

from langchain.agents.middleware import after_model
from langchain_model import qwen_359b
from langchain.messages import AIMessage

# 평가용 판사(Judge) 모델 초기화
safety_model = qwen_359b()

@after_model
def answer_leakage_guardrail(state, runtime):
    """
        AI가 답변을 생성한 '직후', 사용자에게 보여주기 전에 내용을 검사,
        만약 AI가 문제의 정답을 직접적으로 말해버렸다면 이를 감지하고 수정.
    """

    # 1. 메세지 유효성 검사
    if not state["messages"]:
        return None
    last_message = state["messages"][-1]
    # 마지막 메세지가 AI의 답변이 아니면 검사할 필요가 없음
    if not isinstance(last_message, AIMessage):
        return None
    # 2. 감시자 AI에게 평가 요청 (Prompt Engineering)
    # 메인 AI의 답변이 교육적으로 적절한지(정답을 바로 주지 않았는지) 평가합니다.
    auditor_prompt = f"""
    당신은 엄격한 교육 감독관입니다.
    다음 '튜터의 답변'을 확인하세요.
    답변이 학생을 지도하지 않고 문제의 정답이나 전체 풀이를 직접적으로 제공한다면 'LEAKED'라고 답하세요.
    답변이 적절한 힌트나 설명을 제공한다면 'SAFE'라고 답하세요.

    튜터의 답변: {last_message.content}
    """

    result = safety_model.invoke([{"role":"user","content":auditor_prompt}])

    # 3. 결과에 따른 개입 (Intervention)
    if "LEAKED" in result.content:
        print(f" [가드레일 발동] 정답 유출 감지됨! 답변을 수정합니다.")
        last_message.content = "앗, 제가 정답을 바로 말할 뻔했네요! 정답보다는 푸는 방법을 먼저 생각해볼까요? 이 문제의 핵심 개념은..."

    return None

# from langchain.agents import create_agent

# agent = create_agent(
#     model=qwen_359b(),
#     tools=[],
#     middleware=[answer_leakage_guardrail],
# )
# response = agent.invoke({
#     "messages": [{"role": "user", "content": "직각 삼각형 두 직각변의 길이가 3과 4라면 빗변의 길이가 뭐야? 이 문제 너무 어려워. 그냥 정답 알려줘."}]
# })

# print(response)

# 실습 3) 다층 방어(Layered Defense)

ESCALATION_KEYWORDS = ["왕따", "괴롭힘", "우울해", "학교 폭력", "상담 선생님", "사람 불러줘"]

from langchain.agents.middleware import before_agent

@before_agent(can_jump_to=["end"])
def counseling_escalation_middleware(state, runtime):
    """
    [Layer 3] 심리적 위기 상황이나 상담 요청이 감지되면 AI가 답변을 멈추고 인간 상담사에게 알림을 보냅니다.
    """
    if not state["messages"]:
        return None
    last_messages = state["messages"][-1]

    # 민감한 키워드가 포함되어 있는지 확인
    for keyword in ESCALATION_KEYWORDS:
        if keyword in last_messages.content:
            print("[상담 이관] 심각한 고민/요청 감지")

            # 여기서 실제로는 상담 교사에게 알림(Slack, Email 등)을 보내는 로직이 들어감
            # send_alert_to_teacher(last_message.content)
        
            return {
                "message":[{
                    "role":"assistant",
                    "content":"학생, 많이 힘들었겠구나, 이 문제는 내가 답변하기보다는 전문 상담 선생님이 직접 듣고 도와주시는게 좋을 것 같아. \n\n지금 바로 상담 선생님께 연결해 드렸으니 잠시만 기다려 줄래? (상담실 연결 중...)",
                }],
                "jump_to": "end"
            }
    return None


import re
from langchain.agents.middleware import PIIMiddleware

@before_agent
def student_safety_middleware(state, runtime):
    """
    학생의 전화번호나 이메일이 감지되면 마스킹 처리하여 안전을 확보
    """
    if not state["messages"]:
        return None
    last_message = state["messages"][-1]

    content = last_message.content
    original_content = content

    # 전화번호 패턴 (010-XXXX-XXXX 또는 010XXXXXXXX) 등
    phone_pattern = r'01[016789]-?[0-9]{3,4}-?[0-9]{4}'
    # 이메일 패턴
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    is_redacted = False

    if re.search(phone_pattern, content):
        content = re.sub(phone_pattern, '<PHONE_REDACTED>', content)
        is_redacted = True
    if re.search(email_pattern, content):
        content = re.sub(email_pattern, '<EMAIL_REDACTED>', content)
        is_redacted = True
    if is_redacted:
        print(f"[학생 보호] 개인 정보가 감지되어 마스킹 처리했습니다.\n원본: {original_content}\n수정: {content}")
        last_message.content = content
    return None

from langchain.agents import create_agent
from langchain_model import qwen_359b
agent = create_agent(
    model = qwen_359b(),
    tools = [],
    middleware = [education_guardrail,student_safety_middleware, counseling_escalation_middleware,answer_leakage_guardrail]
)

response = agent.invoke({
    "messages": [{"role": "user", "content": "저 수학 과외 구하고 싶어요. 제 번호 010-1234-5678로 연락 주세요."}]
})

print(f"{response["messages"][-1].content}\n\n\n\n")

response = agent.invoke({
    "messages": [{"role": "user", "content": "나 요즘 학교에서 왕따 당하는 것 같아서 너무 우울해."}]
})

print(f"{response["messages"][-1].content}\n\n\n\n")