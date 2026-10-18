확인해 보니 **`content` 폴더에는 PDF만 있고, 학습용 파이썬 파일은 프로젝트 루트와 `5` 폴더에 있습니다.** 해당 파일들을 모두 읽고 정리했어요.

전체적으로 **로컬 모델 호출 → 도구를 쓰는 에이전트 → 메모리와 미들웨어 → PDF 기반 RAG** 순서로 공부하셨습니다. 아래는 코드 내용을 기준으로 한 정리이며, 실행 검증은 하지 않았어요.

**1. 사용한 주요 라이브러리**

| 라이브러리 | 공부한 기능 |
|---|---|
| `langchain` | 모델 초기화, 메시지, 에이전트, 도구, 미들웨어, 구조화 출력 |
| `langchain_core` | 메시지 트리밍, 토큰 수 추정, Document 등 |
| `langchain_community` | PDF·웹 문서 로더 |
| `langchain_text_splitters` | 텍스트와 PDF 청크 분할 |
| `langchain_ollama` | 로컬 임베딩 모델 연결 |
| `langchain_classic` | 임베딩 캐시와 파일 저장소 |
| `langchain_chroma` | 벡터 저장, 유사도 검색, Retriever |
| `langgraph` | 대화 체크포인트와 사용자 메모리 저장소 |
| `pydantic` | 모델 출력 스키마 정의 |
| `requests` | 알라딘 API 요청 |
| `psycopg` | PostgreSQL 연결 |
| 파이썬 기본 모듈 | `dataclasses`, `typing`, `re`, `uuid`, `os`, `pathlib`, `sys`, `time` |

**2. 모델 호출과 메시지 구성**

| 파일 | 공부한 내용 | 만든 것 |
|---|---|---|
| [langchain_model.py](F:/TIL/langchain_first_d/langchain_model.py) | `init_chat_model`, Ollama 연결, `temperature` | Qwen 모델들을 생성하는 공통 함수 |
| [langchain_message.py](F:/TIL/langchain_first_d/langchain_message.py) | `SystemMessage`, `HumanMessage`, `AIMessage`, 딕셔너리 메시지 | 시스템 역할에 따라 다르게 답하는 대화 예제 |
| [langchain_pjt.py](F:/TIL/langchain_first_d/langchain_pjt.py) | `model.batch()` | 여러 입력을 한 번의 배치 호출로 처리하는 예제 |

여기서 공부한 핵심은 **모델 객체 생성, 역할별 메시지 구성, `invoke()`와 `batch()` 사용**이에요.

`batch()`에 넣은 질문들이 자동으로 하나의 연속 대화가 되는 것은 아니고, 각각의 입력을 처리하는 구조입니다.

**3. 도구를 사용하는 에이전트**

| 파일 | 사용한 기능 | 만든 것 |
|---|---|---|
| [langchain_tool.py](F:/TIL/langchain_first_d/langchain_tool.py) | `@tool`, `create_agent` | 지역을 받아 날씨를 알려주는 에이전트 |
| [langchain_calculator.py](F:/TIL/langchain_first_d/langchain_calculator.py) | 여러 도구 등록, 함수 인자 설명 | 덧셈·곱셈·나눗셈 도구를 사용하는 계산 에이전트 |
| [langchain_aladin.py](F:/TIL/langchain_first_d/langchain_aladin.py) | 외부 API를 도구로 연결 | 알라딘 베스트셀러를 조회하는 에이전트 |

구현 수준에는 차이가 있어요.

- **날씨 도구:** 실제 날씨 API 없이 고정된 온도를 반환하는 연습용 코드입니다.
- **계산 도구:** 파이썬 함수로 실제 계산을 수행합니다.
- **알라딘 도구:** 실제 HTTP 요청을 보냅니다. 환경변수 `ALADIN_TTB_KEY`, 타임아웃, HTTP 오류 처리도 넣으셨어요.

즉, **모델이 직접 답하는 방식에서, 필요한 함수를 선택하고 실행 결과를 활용하는 방식으로 확장**하셨습니다.

**4. 답변을 정해진 구조로 받기**

| 파일 | 공부한 내용 | 만든 것 |
|---|---|---|
| [langchain_test.py](F:/TIL/langchain_first_d/langchain_test.py) | `BaseModel`, `Field`, `Optional`, `Literal`, JSON Schema, `with_structured_output()` | 영화 정보를 정해진 필드로 추출하는 예제 |
| [langchain_structure_output.py](F:/TIL/langchain_first_d/langchain_structure_output.py) | `ToolStrategy`, `structured_response`, `model_dump()` | 이메일 의도·감정·요약·다음 조치를 분석하는 에이전트 |

영화 예제에서는 다음 항목을 구조화했어요.

```text
제목 / 개봉 연도 / 장르 / 감독 / 평점
```

이메일 예제에서는 다음 항목을 구조화했어요.

```text
intent / sentiment / summary / next_action
```

그리고 분석 결과가 **부정적인 불만이면 긴급 처리, 일반 문의면 자동 회신 처리**로 분기하도록 작성했습니다.

다만 이메일 읽기·발송은 프로토타입이고, Slack 알림이나 Jira 티켓 생성은 주석과 출력으로 표현한 단계예요.

**5. 단기 메모리와 장기 메모리**

| 파일 | 공부한 내용 | 구현 내용 |
|---|---|---|
| [langchain_memory.py](F:/TIL/langchain_first_d/langchain_memory.py) | `InMemorySaver`, `thread_id` | 같은 대화에서 이름과 앞선 대화를 기억하기 |
| [langchain_memory_strotegy.py](F:/TIL/langchain_first_d/langchain_memory_strotegy.py) | `trim_messages`, `count_tokens_approximately` | 토큰 예산에 맞춰 최근 메시지를 유지하는 예제 |
| [langchain_postgre.py](F:/TIL/langchain_first_d/langchain_postgre.py) | `PostgresSaver`, `psycopg.Connection` | 대화 상태를 PostgreSQL에 저장하도록 연결 |
| [langchain_longtermMemory.py](F:/TIL/langchain_first_d/langchain_longtermMemory.py) | `InMemoryStore`, namespace, `put/get/search`, 메모리 주입 | 사용자 정보와 선호도를 저장·조회하는 예제 |

여기서는 서로 다른 두 종류의 기억을 공부했어요.

```text
단기 메모리:
thread_id를 기준으로 대화 상태를 이어감

장기 메모리:
사용자 ID와 앱 이름을 기준으로 별도 정보를 저장하고 꺼냄
```

장기 메모리 파일에는 두 가지 접근이 있습니다.

- **미들웨어 방식:** 저장된 정보를 검색해 시스템 프롬프트에 넣기
- **도구 방식:** 모델이 사용자 정보 저장·조회 도구를 호출하기

단, `InMemoryStore`는 메모리 저장소여서 **프로세스를 종료한 뒤에도 정보가 남는 영구 저장은 아닙니다.**

메모리 전략 파일의 **요약 + 최근 대화, 상태 구조화, 검색 기반 메모리**는 제목만 적혀 있고 구현은 아직 없습니다.

**6. 런타임 컨텍스트와 커스텀 미들웨어**

| 파일 | 공부한 내용 | 구현 내용 |
|---|---|---|
| [langchain_runtime_state.py](F:/TIL/langchain_first_d/langchain_runtime_state.py) | `Context`, `runtime.context`, `before_model`, `wrap_model_call`, `request.override()` | 사용자 이름을 프롬프트에 주입하고 메시지 길이에 따라 모델 선택 |
| [langchain_custom_middleware.py](F:/TIL/langchain_first_d/langchain_custom_middleware.py) | 입력 차단, 실행 중단, 모델 라우팅 | 금지어 차단, 입력 길이별 모델 선택, 회원 등급별 모델 선택 |

구체적으로 다음을 연습하셨어요.

- `state["messages"]`로 현재 대화 읽기
- `runtime.context`로 이름·회원 정보 읽기
- `request.override(model=...)`로 호출할 모델 바꾸기
- 시스템 메시지에 사용자 이름 넣기
- `handler(new_request)`로 수정한 요청 전달하기
- `jump_to="end"`로 모델 호출 전에 실행 끝내기

현재 파일 상태를 보면:

- `langchain_runtime_state.py`는 **이름 주입 미들웨어만 등록**되어 있습니다.
- 길이별 모델 선택 함수는 정의되어 있지만 현재 에이전트에 등록되어 있지 않습니다.
- `langchain_custom_middleware.py`는 **회원 등급별 모델 선택 코드가 활성화**되어 있고, 앞선 예제들은 주석입니다.

**7. 내장 미들웨어와 교육용 가드레일**

[langchain_builtin_middleware.py](F:/TIL/langchain_first_d/langchain_builtin_middleware.py)에서는 다음 기능을 실습했습니다.

| 미들웨어 | 공부한 목적 |
|---|---|
| `LLMToolEmulator` | 실제 도구 실행 대신 LLM으로 도구 결과를 모의 생성 |
| `TodoListMiddleware` | 여러 단계의 작업 계획과 진행 관리 |
| `HumanInTheLoopMiddleware` | 이메일 발송 전에 승인·수정·거절 받기 |
| `PIIMiddleware` | 이메일·카드번호·전화번호·API 키 탐지 및 처리 |

전화번호에는 정규식 탐지기를, API 키에는 직접 작성한 탐지 함수를 사용했어요. 여러 예제의 호출 부분은 주석 처리되어 있습니다.

[langchain_guardrail.py](F:/TIL/langchain_first_d/langchain_guardrail.py)에서는 **여러 보호 단계를 가진 교육용 튜터 에이전트**를 구성했습니다.

| 처리 단계 | 구현한 기능 |
|---|---|
| 입력 검사 | 숙제 대행·부정행위 관련 키워드 차단 |
| 주제 관리 | 게임 등 학습 외 주제에 학습 안내 반환 |
| 개인정보 처리 | 전화번호·이메일을 대체 문자열로 변경 |
| 상담 요청 감지 | 특정 키워드 감지 시 상담 이관 안내 |
| 출력 검사 | 별도 모델로 정답 유출 여부 평가 후 답변 변경 |

상담 이관은 **안내 문구와 출력까지만 구현**되어 있고, 실제 상담사에게 연결하거나 알림을 보내는 기능은 없습니다.

**8. PDF 기반 RAG — 최근 공부한 부분**

`5` 폴더에서는 **문서 로딩부터 검색 결과를 활용한 답변 생성까지** 연결하셨어요.

| 파일 | 사용한 모듈 | 공부·구현한 내용 |
|---|---|---|
| [langchain_load.py](F:/TIL/langchain_first_d/5/langchain_load.py) | `PDFPlumberLoader`, `PyMuPDFLoader`, `WebBaseLoader`, `HwpHwpxLoader` | PDF·웹·한글 문서 로딩 예제. 현재는 전체 주석 |
| [langchain_split.py](F:/TIL/langchain_first_d/5/langchain_split.py) | `RecursiveCharacterTextSplitter`, `CharacterTextSplitter` | 문자열 분할 비교 및 실제 PDF 분할 |
| [langchain_embed.py](F:/TIL/langchain_first_d/5/langchain_embed.py) | `OllamaEmbeddings`, `CacheBackedEmbeddings`, `LocalFileStore` | 임베딩과 파일 캐시 설정 |
| [langchain_store.py](F:/TIL/langchain_first_d/5/langchain_store.py) | `Chroma` | PDF 청크를 임베딩해서 저장하고 유사 문서 검색 |
| [langchain_retrieve.py](F:/TIL/langchain_first_d/5/langchain_retrieve.py) | Retriever, 메시지, Qwen 모델 | 검색한 PDF 내용을 프롬프트에 넣어 답변 생성 |

현재 연결한 전체 흐름은 이렇습니다.

```text
ARKK 보유 종목 PDF
    ↓ PDFPlumberLoader
문서 로딩
    ↓ RecursiveCharacterTextSplitter
1000자 / 겹침 150자로 분할
    ↓ qwen3-embedding:0.6b
청크 임베딩
    ↓ CacheBackedEmbeddings + LocalFileStore
임베딩 캐시
    ↓ Chroma
벡터 저장
    ↓ Retriever
질문과 관련된 청크 검색
    ↓ SystemMessage에 검색 내용 삽입
qwen3.5:9b로 답변 생성
```

검색 방식도 여러 개를 공부했습니다.

- **유사도 검색:** 비슷한 청크 `k`개 반환
- **점수 임계값 검색:** 일정 관련성 점수를 넘는 청크 반환
- **MMR 검색:** 질문 관련성과 결과 다양성을 함께 고려

현재 검색 파일은 **임계값 `0.3`을 사용하는 검색이 활성화**되어 있고, MMR 설정은 주석으로 남아 있습니다.

**9. 복습할 때 함께 확인하면 좋은 코드 상태**

학습 기록과 현재 동작을 혼동하지 않도록, 눈에 띈 부분도 적어둘게요.

| 위치 | 확인할 부분 |
|---|---|
| 커스텀 미들웨어 | `model=qwen_3508b`로 함수 자체를 전달합니다. 모델 객체를 전달하려는 코드라면 `qwen_3508b()` 호출이 필요합니다. |
| 런타임 이름 주입 | 이름이 비어 있으면 `new_request`가 만들어지지 않은 채 사용됩니다. |
| 장기 메모리 | 저장 시 `personal_assistance`, 조회 시 `personal_assistant`로 앱 이름이 달라 서로 다른 namespace를 조회합니다. |
| 장기 메모리 도구 | `runtime`에 `ToolRuntime` 타입 지정이 빠져 있습니다. |
| HITL 예제 | `InMemorySaver()`를 만들었지만 해당 에이전트에 `checkpointer`로 전달하지 않았습니다. |
| 상담 이관 | 반환 키가 `"messages"`가 아닌 `"message"`로 되어 있습니다. |
| 임베딩 예제 | `langchain_embed.py`에는 캐시 namespace의 `:`가 남아 있고, 저장·검색 파일에서는 `_`로 수정되어 있습니다. |
| 검색 예제 | `langchain_split`을 import하면 그 파일의 PDF 로딩·분할 코드도 실행됩니다. |
| Chroma 거리 설정 | 저장 코드와 검색 코드의 거리 설정이 다릅니다. 기존 컬렉션을 불러오면서 설정만 추가했다고 거리 기준이 바뀌는 것은 아닙니다. |

현재까지 작성한 결과물은 크게 **계산 도구 에이전트, 베스트셀러 조회 에이전트, 이메일 분석 프로토타입, 사용자 메모리 예제, 교육용 튜터 가드레일, ARKK PDF 질의응답 RAG**로 정리할 수 있습니다.
