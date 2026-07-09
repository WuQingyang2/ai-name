from fastapi import APIRouter, Depends
from schemas.question_schemas import InterviewQuestionIn, InterviewQuestionOut
from core.agent import generate_interview_questions
from core.auth import AuthHandler

auth_handler = AuthHandler()

router = APIRouter(prefix="/question", tags=["面试题相关接口"])

@router.post("/", response_model=InterviewQuestionOut)
async def take_interview_questions(
    data: InterviewQuestionIn, 
    user_id: int=Depends(auth_handler.auth_access_dependency)
):
    question_result = await generate_interview_questions(data)
    return InterviewQuestionOut(questions=question_result.questions)