from abc import ABC, abstractmethod

from logger.logger_back import logger
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def add_many(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def find_many(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    """
    Конкретный класс работы с БД От него наследуются остальные репозитории
    """
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, values: BaseModel) -> bool:
        """
        Добавление одной новой записи в БД
        :param values: Объект класса модели БД
        :return:
        """
        try:
            self.session.add(values)
            return True
        except Exception as ex:
            logger.error(f'Функция add_one в слое repository. Ошибка добавления данных в БД  \n{ex}\n')
            return False

    async def add_many(self, values: list) -> bool:
        """
        Добавление множества значений в БД
        :param values: Список из объектов моделей.
        :return:
        """
        try:
            self.session.add_all(values)
            return True
        except Exception as ex:
            logger.error(f'Функция add_many в слое repository. Ошибка добавления данных в БД \n{ex}\n')
            return False

    async def update(self, values: dict, filters: dict | None) -> list | bool:
        """
        Обновление данных в БД
        :param values: dict с меняемыми значениями {<название столбца>:<новое значение столбца>}
        :param filters: dict с фильтрами {<название столбца>:<значение столбца>}
        :return: Возвращает список с кортежами id который обновлялись [(<id>,), (<id>,)] False в случае ошибки
        """
        try:
            stmt = update(self.model).values(**values).returning(self.model.id)
            if filters:
                stmt = stmt.filter_by(**filters)

            response_db = await self.session.execute(stmt)
        except Exception as ex:
            logger.error(f'Функция update в слое repository. Ошибка обновления данных в БД \n{ex}\n')
            return False
        return response_db.all()

    async def find_all(self) -> list | bool:
        """
        Взятие всех значений из БД
        :return: возвращает список объектов
        """
        try:
            stmt = select(self.model)
            res = await self.session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
        except Exception as ex:
            logger.error(f'Функция find_all в слое repository. Ошибка получения данных из БД или преобразовании из \n{ex}\n')
            return False
        return res

    async def find_many(self, filters: dict | None) -> list | bool:
        """
        Взятие значений из БД по фильтрам
        :param filters: dict с фильтрами {<название столбца>:<значение столбца>}
        :return: возвращает список объектов
        """
        try:
            stmt = select(self.model)
            if filters:
                stmt = stmt.filter_by(**filters)
            res = await self.session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
        except Exception as ex:
            logger.error(f'Функция find_many в слое repository. Ошибка получения данных из БД или применении фильтров \n{ex}\n')
            return False
        return res
