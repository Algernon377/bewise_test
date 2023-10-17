from DB.schemas.quiz_questions_schemas import QuizQuestionsAddSchema, \
    QuizQuestionsAddManySchema, QuizQuestionsUpdateSchema
from DB.services.base_service import BaseService
from DB.models.quiz_questions_model import QuizQuestionsModel
from logger.logger_back import logger


class QuizQuestionsService(BaseService):

    async def add_one(self, quiz_questions_data: QuizQuestionsAddSchema) -> QuizQuestionsModel | bool:
        """
        Добавляет объект в БД
        :param quiz_questions_data:
        :return: Возвращает или объект модели или False
        """
        try:
            quiz_questions_dict = quiz_questions_data.model_dump()
            quiz_questions_obj = QuizQuestionsModel(**quiz_questions_dict)
        except Exception as ex:
            logger.error(f'Функция add_one в слое service. Ошибка получения данных \n{ex}\n')
            return False

        resp = await self.repository.add_one(quiz_questions_obj)
        if resp:
            return quiz_questions_obj
        return False

    async def add_many(self, list_quiz_questions_data: QuizQuestionsAddManySchema) -> list[QuizQuestionsModel] | bool:
        """
        Добавляет объекты в БД
        :param list_quiz_questions_data: list с объектами модели
        :return: Возвращает или список объектов модели или False
        """
        try:
            quiz_questions_list = [QuizQuestionsModel(**_.model_dump()) for _ in list_quiz_questions_data.list_obj]
        except Exception as ex:
            logger.error(f'Функция add_many в слое service. Ошибка получения данных \n{ex}\n')
            return False

        resp = await self.repository.add_many(quiz_questions_list)
        if resp:
            return quiz_questions_list
        return False

    async def update(self, list_quiz_questions_data: QuizQuestionsUpdateSchema) -> list | bool:
        """
        Обновляет объекты в БД
        :param list_quiz_questions_data:
        :return: Возвращает список с кортежами id который обновлялись [(<id>,), (<id>,)] False в случае ошибки
        """
        try:
            filters = list_quiz_questions_data.filters
            update_data = list_quiz_questions_data.value
        except Exception as ex:
            logger.error(f'Функция update в слое service. Ошибка получения данных \n{ex}\n')
            return False

        response_db = await self.repository.update(update_data, filters)
        return response_db


