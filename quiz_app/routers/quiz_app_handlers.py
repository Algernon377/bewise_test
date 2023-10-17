from DB.schemas.quiz_questions_schemas import QuizQuestionsPostManyResponse, QuizQuestionsPostRequest
from fastapi import APIRouter, HTTPException, Request
from quiz_app.business_logic.questions_with_answers_logic.quiz_app_logic import request_questions_with_answers

router = APIRouter(tags=['quiz'])


@router.post("/quiz/", response_model=QuizQuestionsPostManyResponse)
async def returns_questions_with_answers(post_questions_num: QuizQuestionsPostRequest, request: Request):
    if post_questions_num.questions_num < 1:
        raise HTTPException(status_code=404, detail="Значение запрашиваемых вопросов должно быть не меньше 1")
    previous_questions = await request_questions_with_answers(post_questions_num.questions_num, request)

    if previous_questions is False:
        raise HTTPException(status_code=500, detail="Database error")

    if previous_questions or isinstance(previous_questions, list):
        return {'response_by_db': previous_questions}

    return {'response_by_db': False}

