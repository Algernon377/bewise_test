import datetime

from DB.models.base_model import Base
from DB.schemas.quiz_questions_schemas import QuizQuestionsSchema
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional
from sqlalchemy import String, DateTime, Integer, BigInteger
from sqlalchemy.sql import func


class QuizQuestionsModel(Base):
    """
    Класс для таблицы quiz_questions
    При добавлении нового столбца обязательно анатируем, на этом завязано извлечение списка всех столбцов
    Если анотировать необходимо что-то помимо столбца, необходимо переписать логику извлечения имен столбцов
    """
    __tablename__ = 'quiz_questions'

    question_id: Mapped[int] = mapped_column(BigInteger)
    question: Mapped[str] = mapped_column(String)
    answer: Mapped[str] = mapped_column(String(200))
    question_creation_date: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    recipient_ip: Mapped[Optional[str]] = mapped_column(String(50))

    def to_read_model(self) -> QuizQuestionsSchema:
        return QuizQuestionsSchema(
            id=self.id,
            question_id=self.question_id,
            question=self.question,
            answer=self.answer,
            question_creation_date=self.question_creation_date,
            recipient_ip=self.recipient_ip
        )
