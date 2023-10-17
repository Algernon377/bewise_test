from DB.DB_manager import async_session_maker
from DB.repositories.quiz_questions_repositories import QuizQuestionsRepository
from DB.schemas.quiz_questions_schemas import QuizQuestionsPostSchema, QuizQuestionsAddManySchema, \
    QuizQuestionsUpdateSchema
from DB.utils.UnitOfWork import UnitOfWork
from fastapi import Request
from DB.services.quiz_questions_service import QuizQuestionsService


async def requests_free_questions_from_db(request: Request) -> list:
    """
    Берет из БД вопросы которые были получены из предыдущего запроса,
    добавляет взятым записям ip пользователя кому отправляются вопросы.
    :param request:
    :return: список с вопросами
    """
    filters_dict = {'recipient_ip': None}
    filters = QuizQuestionsPostSchema(filters_dict=filters_dict)
    async with UnitOfWork(async_session_maker) as uow:
        response_by_db = await QuizQuestionsService(QuizQuestionsRepository(uow.session)).find_many(filters=filters)
    if response_by_db:
        async with UnitOfWork(async_session_maker) as uow:
            value = {'recipient_ip': request.client.host}
            update_data = QuizQuestionsUpdateSchema(filters=filters_dict, value=value)
            response_by_db_update = await QuizQuestionsService(QuizQuestionsRepository(uow.session)).update(update_data)
            await uow.commit()
    return response_by_db


async def save_new_questions_in_db(new_questions: list) -> list:
    """
    Сохраняет в БД новые вопросы
    :param new_questions: Список новых вопросов [QuizQuestionsAddSchema,QuizQuestionsAddSchema...]
    :return:
    """
    questions_objects = QuizQuestionsAddManySchema(list_obj=new_questions)
    async with UnitOfWork(async_session_maker) as uow:
        response_by_db = await QuizQuestionsService(QuizQuestionsRepository(uow.session)).add_many(questions_objects)
        await uow.commit()
    return response_by_db

