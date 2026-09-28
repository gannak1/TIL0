from langchain.tools import tool
from typing import List, Dict

@tool
def send_email_tool(to:str, subject:str, body:str)->str:
    """지정한 이메일 주소로 메일을 보내는 도구(프로토 타입)"""
    return f"✅ 이메일이 성공적으로 전송되었습니다.\n수신자: {to}\n제목: {subject}\n내용: {body[:50]}..."

@tool
def read_email_tool(limit: int = 1) -> List[Dict[str, str]]:
    """가상의 고객 이메일을 조회하는 도구."""
    return f"✅ 이메일이 성공적으로 조회되었습니다."

# 스키마 설계
from pydantic import BaseModel, Field
from typing import Literal

class EmailAnalysis(BaseModel):
    """이메일 내용을 분석한 결과 구조"""

    intent: Literal["complaint", "inquiry", "confirmation","other"] = Field(
        description = "이메일의 주요 의도 (complaint=불만, inquiry=문의, confirmation=확인, other=기타)"
    )

    sentiment: Literal["positive","negative","neutral"] = Field(
        description = "고객의 감정 상태"
    )

    summary:str = Field(
        description = "이메일의 핵심 내용을 1~2문자응로 짧게 요약"
    )

    next_action:str = Field(
        description="담당자가 취해야할 다음 단계 (예: 환불 부서 이관, 메뉴얼 링크 발송 등)"
    )

from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolEmulator
from langchain.agents.structured_output import ToolStrategy
from langchain.chat_models import init_chat_model
from langchain_model import qwen_359b

model = qwen_359b()
tools = [send_email_tool, read_email_tool]

agent = create_agent(
    model = model,
    tools= tools,
    response_format = ToolStrategy(EmailAnalysis),
    middleware=[LLMToolEmulator(model=qwen_359b())],
)

response = agent.invoke(
    {
        "messages":[{
            "role":"user",
            "content":"최근 온 메일을 읽고 고객의 의도와 감정, 요약, 그리고 필요한 다음 조치를 분석해줘."
        }]
    }
)

analysis = response["structured_response"]
print(analysis)

# Pydantic 객체를 딕셔너리로 변환
data_for_db = analysis.model_dump()

# 구조화된 스키마 데이터를 기반으로 한 자동화 파이프라인 예시
if data_for_db["intent"] == "complaint" and data_for_db["sentiment"] == "negative":
    # 1. CS팀 슬랙 채널에 긴급 알림 전송 (API 호출)
    # 2. Jira 이슈 트래커에 '긴급(High)' 티켓 자동 생성
    print("🚨 [긴급] 불만 접수! CS팀에 즉시 알림을 전송합니다.")
    print(f"요약: {data_for_db['summary']}")
elif data_for_db["intent"] == "inquiry":
    # FAQ 데이터베이스 검색 후 자동 회신 스크립트 실행
    print("ℹ️ 일반 문의 접수. 자동 회신 프로세스를 시작합니다.")