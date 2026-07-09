from pydantic import BaseModel, Field
from typing import Annotated, List

class QuestionSchema(BaseModel):
    question: Annotated[str, Field(..., description="问题")]
    points: Annotated[List[str], Field([], description="考察点")]

class QuestionResultSchema(BaseModel):
    questions: List[QuestionSchema]
