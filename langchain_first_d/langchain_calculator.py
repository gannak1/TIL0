from langchain.tools import tool
from langchain_model import *
from langchain.agents import create_agent
import time

c = time.time()

@tool
def add(a:int, b:int)->int:
    """
    `a`와`b`의 덧셈

    Args :
        a : First int
        b : Second int
    """
    return a + b

@tool
def multiply(a:int, b:int)->int:
    """
    `a`와`b`의 곱셈

    Args :
        a : First int
        b : Second int
    """
    return a * b

@tool
def divide(a:int, b:int)->int:
    """
    `a`와`b`의 나눗셈

    Args :
        a : First int
        b : Second int
    """
    return a / b


agent = create_agent(model = qwen_359b(), tools = [add, multiply, divide])

result = agent.invoke(
    {"messages":[{"role":"user","content":"42 + 3 * 23 은 뭔가요?"}]}
)

print(result)


print(f"\n\n{time.time()-c}")