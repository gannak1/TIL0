from pydantic import BaseModel, Field
from typing import Optional, Literal
from langchain.chat_models import init_chat_model


class Movie(BaseModel):
    """상세한 영화 정보"""
    title:str = Field(description="영화의 제목")
    year:Optional[int] = Field(default = None, description = "개봉 연도, 정보를 알 수 없다면 None")
    genre: Literal["액션","로맨스","SF","로맨스","코미디","기타"] = Field(description="영화의 장르")
    director: str = Field(description = "영화 감독 이름")
    rating: float = Field(description="영화 평점 (10점 만점 기준)")


json_schema = {
    "title" : "Movie",
    "description" : "A movie with detail",
    "type" : "object",
    "properties" : {
        "title" : {
            "type": "string",
            "description" : "The title of the movie",
        },
        "year" : {
            "type" : "integer",
            "description" : "The year the movie was released",
        },
        "director": {
            "type" : "string",
            "description"  :"The director of the movie",
        },
        "rating": {
            "type" : "number",
            "description" : "The movie's rating out of 10"
}
    },
    "required" : ["title","director","rating"]
}

model = init_chat_model(model = "qwen3:14b", model_provider="ollama")
model_with_structure = model.with_structured_output(Movie)

response = model_with_structure.invoke("영화 인셉션에 대해 설명")

print("class 형태 스키마 출력")
print(response)

model_with_structure = model.with_structured_output(json_schema)

response = model_with_structure.invoke("영화 인셉션에 대해 설명")

print("json 형태 스키마 출력")
print(response)