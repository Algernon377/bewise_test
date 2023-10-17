from fastapi import Request
from logger.logger_back import logger

from quiz_app.business_logic.questions_with_answers_logic.db_worker import requests_free_questions_from_db, \
    save_new_questions_in_db
from quiz_app.business_logic.questions_with_answers_logic.scrapper import requests_new_questions_from_url


async def request_questions_with_answers(questions_num: int, request: Request) -> list | bool:
    """
    Запрашивает вопросы с URL, сохраняет в БД, возвращает список вопросов из предыдущего запроса
    :param questions_num: int сколько вопросов запросить с url
    :param request:
    :return: список вопросов из предыдущего запроса, False в случае ошибки
    """
    try:
        questions_from_db = await requests_free_questions_from_db(request)
        new_questions = await requests_new_questions_from_url(questions_num)
        saved_obj_list = await save_new_questions_in_db(new_questions)
        return questions_from_db
    except Exception as ex:
        logger.error(f'Ошибка в работе функции request_questions_with_answers \n{ex}\n')
        return False


