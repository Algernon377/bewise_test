from DB.repositories.base_repository import AbstractRepository
from logger.logger_back import logger


class BaseService:
    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository

    async def get_all(self):
        rows = await self.repository.find_all()
        return rows

    async def find_many(self, filters):
        try:
            filters = filters.filters_dict
        except Exception as ex:
            logger.error(f'Функция find_many в слое service. Ошибка получения данных \n{ex}\n')
            return False
        rows = await self.repository.find_many(filters)
        return rows
