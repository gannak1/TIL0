from langchain_model import qwen_359b
import requests
from langchain.tools import tool
from typing import Dict, List, Any, Union
import os

def require_env(key_name:str)->str:
    value = os.environ.get(key_name)
    if not value:
        raise RuntimeError(f"필수 환경 변수가 없습니다: {key_name}")
    else:
        return value

@tool
def fetch_aladin_bestseller_top10() -> Union[List[Dict[str, Any]],str]:
    """
    현재 시점의 알라딘 베스트셀러 Top 10 도서 목록을 조회하여 반환한다.
    반환값은 도서 정보가 담긴 딕셔너리의 리스트이거나, 호출 실패 시 에러 메세지(문자열)이다.
    """
    try:
        ttb_key = require_env("ALADIN_TTB_KEY")
        url = "http://www.aladin.co.kr/ttb/api/ItemList.aspx"
        params = {
            "ttbkey": ttb_key,
            "QueryType": "Bestseller",
            "MaxResults": 10,
            "start": 1,
            "SearchTarget": "Book",
            "output": "js",
            "Version": "20131101",
        }

        # API 호출 ( 타임아웃 10초 설정으로 무한 대기 방지)
        resp = requests.get(url, params = params, timeout = 10)

        resp.raise_for_status() # HTTP 4xx, 5xx 에러 발생 시 예외 발생

        data = resp.json()

        # 모델이 핵심 정보에만 집중할 수 있도록, 전체 응답 중 도서 목록 10개만 슬라이싱하여 반환 (토큰 다이어트)
        return data.get("item",[])[:10]
    except Exception as e:
        # 에러가 발생해도 프로그램이 종료되지 않고, 모델에게 실패 원인을 텍스트로 알려줌 (우아한 실패)
        return f"API 호출 중 오류가 발생하여 베스트셀러 정보를 가져오지 못했습니다. 원인 : {str(e)}"

from langchain.agents import create_agent

model = qwen_359b()
agent = create_agent(model = model, tools = [fetch_aladin_bestseller_top10], system_prompt="너는 한국인이므로 한국어로 대답해야해")

response = agent.invoke( {
    "messages": [
        {"role" : "user","content":"지금 알라딘 베스트셀러 1위부터 3위까지 알려줘"}
    ]
})
print(response["messages"][-1].content)