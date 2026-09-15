from langchain.chat_models import init_chat_model


model = init_chat_model(model = "qwen3:14b",model_provider = "ollama",temperature = 0.7)

inputs = ["흰눈이의 정체를 알려줘",
          "흰눈이가 뭐라고 했지?",
          "악의 정점이자 냄새의 신"
]

responses = model.batch(inputs)

for i, response in enumerate(responses):
    print(f"[{i+1}번째 답변] : {response.content}")