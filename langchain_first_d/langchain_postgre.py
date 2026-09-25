from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg import Connection
from langchain_model import qwen_359b

# 1. 중앙 DB 연결 설정
DB_URI = "postgresql://user:password@localhost:5432/agent_db"
conn = Connection.connect(DB_URI)

# 2. RDB 기반의 체크포인터 생성
db_checkpointer = PostgresSaver(conn)
db_checkpointer.setup() # 상태 저장을 위한 내부 테이블 자동 생성

model = qwen_359b()

tools = []

# 3. 에이전트에 영구 저장소 주입
agent = create_agent(
    model,
    tools,
    checkpointer=db_checkpointer,
)