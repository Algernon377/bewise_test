import datetime

from pydantic import BaseModel
from typing import Optional, Dict, Tuple, List


class QuizQuestionsSchema(BaseModel):
    id: int
    question_id: int
    question: str
    answer: str
    question_creation_date: Optional[datetime.datetime] = None
    recipient_ip: Optional[str] = None

    class Config:
        from_attributes = True

class QuizQuestionsPostSchema(BaseModel):
    filters_dict: Dict


class QuizQuestionsAddSchema(BaseModel):
    question_id: int
    question: str
    answer: str
    recipient_ip: Optional[str] = None

class QuizQuestionsAddManySchema(BaseModel):
    list_obj: List[QuizQuestionsAddSchema]


class QuizQuestionsUpdateSchema(BaseModel):
    value: Dict
    filters: Optional[Dict] = None


class QuizQuestionsPostRequest(BaseModel):
    questions_num: int



class QuizQuestionsPostResponse(BaseModel):
    response_by_db: int | bool

class QuizQuestionsPostManyResponse(BaseModel):
    response_by_db: list | bool

class QuizQuestionsGetResponse(BaseModel):
    response_by_db: List[Tuple] | bool

class QuizQuestionsPutResponse(BaseModel):
    response_by_db: Dict | bool

