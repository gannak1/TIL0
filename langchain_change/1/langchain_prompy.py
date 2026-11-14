from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

model = init_chat_model(model = "qwen3.5:9b",model_provider="ollama", temperature=0.7)

template = PromptTemplate.from_template('''아래 작성한 컨텍스트(Context)를 기반으로 질문(Question)에 대답하세요. 제공된 정보로 대답할 수 없는 질문이라면 "모르겠어요. " 라고 답하세요.

Context : {Context}

Question : {question}

Answer: ''', model = model)

prompt = template.invoke({
    "Context": '''거대 언어 모델(LLM)은 자연어 처리(NLP) 분ㅇ야의 최신 발전을 이끌고 있습니다.
    거대 언어 모델은 더 작은 모델보다 우수한 성능을 보이며,
    NLP 기능을 갖춘 애플리케이션읠 개발하는 개발자들에게 
    매우 중요한 도구가 되었습니다. 개발자들은 Hugging Face의 
    'transformers' 라이브러리를 활용하거나, 
    'openai' 및 'cohere'라는 라이브러리를 통해 OpenAI와 
    Cohere의 서비스를 이용하여 거대 언어 모델을 활용할 수 있습니다.''',
    'question': '거대 언어 모델은 어디서 제공하나요?'
})

completion = model.invoke(prompt)

print(completion)