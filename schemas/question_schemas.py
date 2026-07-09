from pydantic import BaseModel, Field
from typing import Annotated, List, Literal
from .agent_schemas import QuestionSchema

class InterviewQuestionIn(BaseModel):
    job_title: Annotated[str, Field(..., description="职位名称")]
    seniority: Annotated[Literal["不限", "初级", "中级", "高级"], Field(..., description="级别")]
    company_type: Annotated[str, Field(..., description="公司类型")]
    tech_stack: Annotated[List[str], Field([], description="技术栈")]
    question_count: Annotated[int, Field(..., description="问题数量")]
    other: Annotated[str|None, Field("", description="其他要求")]

class InterviewQuestionOut(BaseModel):
    questions: List[QuestionSchema]