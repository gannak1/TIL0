from langchain.chat_models import init_chat_model

def qwen_3827bq4(model="",temperature:float=0.7):
    return init_chat_model(model="qwen3.8:27b-q4_K_M",model_provider="ollama",temperature=temperature)

def qwen_3827bq3(temperature:float=0.7):
    return init_chat_model(model="hf.co/Chungulus/Qwen3.8-27B-Q3_K_M-GGUF:Q3_K_M",model_provider="ollama",temperature=temperature)

def qwen_359b(temperature:float=0.7):
    return init_chat_model(model="qwen3.5:9b",model_provider="ollama",temperature=temperature)

def qwen_3508b(temperature:float=0.7):
    return init_chat_model(model="qwen3.5:0.8b",model_provider="ollama",temperature=temperature)