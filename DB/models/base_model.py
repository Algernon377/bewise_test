from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    __tablename__ = None
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    pass
