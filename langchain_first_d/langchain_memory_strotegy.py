from langchain.chat_models import init_chat_model


model = init_chat_model(model= "qwen3:14b", model_provider="ollama",temperature=0.7)


# 1. 슬라이딩 윈도우 대화를 최근 순으로 몇개로 잘라서 전달
init_message = [
    {"role":"system","content":""},
    {"role":"system","content":""},
    {"role":"system","content":""},
    {"role":"system","content":""},
    {"role":"system","content":""}
]

response = model.invoke(init_message)
print("1. 슬라이딩 윈도우 : ")
print(response.content)

# 2. 토큰 예산 기반 트리밍 (권장 기본값)

from langchain_core.messages.utils import trim_messages, count_tokens_approximately

messages = [
    {"role":"system","content":""},
    {"role":"system","content":""},
    {"role":"system","content":""},
    {"role":"system","content":""},
    {"role":"system","content":""},
    {"role":"system","content":""},
]

trimed_messages = trim_messages(
    messages,
    strategy = "last", # 오래된 대화를 버리고 최근 대화를 유지
    token_counter = count_tokens_approximately,
    max_tokens = 2000,
    include_system = True, # 시스템 메세지는 잘려나가지 않도록 고정(핀)
    start_on = "human", # 잘라 냈을 때 첫 시작이 무조건 사람 질문이 되도록 보정
    end_on = ("human","tool"), # 마지막 질문이 다음과 같도록 보정
)

response = model.invoke(trimed_messages)

# 3. 요약 + 최근대화 유지 (하이브리드)

# 4. 상태 분리 및 구조화

# 5. 검색 기반 메모리 (RAG 활용)