import json
import os
import httpx

from fastapi import Request
from dotenv import load_dotenv

from DB.DB_manager import async_session_maker
from DB.repositories.quiz_questions_repositories import QuizQuestionsRepository
from DB.schemas.quiz_questions_schemas import QuizQuestionsAddSchema
from DB.services.quiz_questions_service import QuizQuestionsService
from DB.utils.UnitOfWork import UnitOfWork

load_dotenv()
URL_QUESTIONS = os.getenv('URL_QUESTIONS')


async def requests_new_questions_from_url(questions_num: int):
    """
    Запрашивает id всех вопросов из БД,
    после этого делает запрос к url проверяет на совпадение. Е
    сли вопроса с таким id нет в БД, добавляет в список который возвращает.
    :param questions_num: int сколько вопросов нужно вернуть
    :return: возвращает список объектов (схем pydantic)
    """
    all_id_questions = await request_all_id_questions_from_db()
    questions_for_db = []
    while len(questions_for_db) != questions_num:
        raw_questions = await request_questions_from_url(questions_num*2)
        questions_obj = await parsing_and_transformation_questions(raw_questions)
        for quest in questions_obj:
            if quest.question_id not in all_id_questions:
                questions_for_db.append(quest)
                if len(questions_for_db) == questions_num:
                    break
    return questions_for_db


async def request_all_id_questions_from_db() -> list:
    """
    Запрашивает все записи из БД, создает список со всеми question_id
    :return: [int,int...] - список со всеми question_id в БД
    """
    async with UnitOfWork(async_session_maker) as uow:
        response_by_db = await QuizQuestionsService(QuizQuestionsRepository(uow.session)).get_all()
    return [row.question_id for row in response_by_db]


async def request_questions_from_url(questions_num: int) -> list:
    """
    Запрашивает вопросы с URL, преобразует ответ в list
    :param questions_num: int - количество запрашиваемых вопросов
    :return: [dict,dict...] - список с вопросами в формате dict
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{URL_QUESTIONS}{questions_num}")
        raw_questions = json.loads(response.content.decode('utf-8'))
        return raw_questions


async def parsing_and_transformation_questions(raw_questions: list[dict]) -> list:
    """
    Преобразует получаемый список с dict вопросами в список с объектами pydantic(схем pydantic)
    :param raw_questions:
    :return: [QuizQuestionsAddSchema,QuizQuestionsAddSchema ...]
    """
    questions = []
    new_row = {}
    for row in raw_questions:
        new_row['question_id'] = row.get('id')
        new_row['question'] = row.get('question')
        new_row['answer'] = row.get('answer')
        questions.append(QuizQuestionsAddSchema(**new_row))
    return questions

