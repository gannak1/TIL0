import sys
from pathlib import Path

# 부모 Path 추가
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_model import qwen_359b
from langchain.tools import tool

# 1. 뇌(LLM) 준비
model = qwen_359b()

# 2. 손발(도구) 정의
@tool
def multiply(a:int, b:int):
    """Multiply `a` and `b`
    Args:
        a: First int
        b: Second int    
    """
    return a * b

@tool
def add(a:int, b:int)->int:
    """Add `a`` and `b`
    Args:
        a: First int
        b: Second int
    """
    return a + b

@tool
def divide(a:int, b:int)->float:
    """Divide `a`` and `b`
    Args:
        a: First int
        b: Second int
    """
    return a / b

