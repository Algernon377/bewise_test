from DB.repositories.base_repository import SQLAlchemyRepository
from DB.models.quiz_questions_model import QuizQuestionsModel


class QuizQuestionsRepository(SQLAlchemyRepository):
    model = QuizQuestionsModel
