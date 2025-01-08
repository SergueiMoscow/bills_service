from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Double
from datetime import datetime, timezone

from db.db import Base


class Cheque(Base):
    __tablename__ = 'cheques'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String, nullable=True)  # Имя файла чека json
    purchase_date = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))  # Дата и время покупки
    user = Column(String, nullable=False)  # Отправитель
    seller = Column(String, nullable=False, default='')
    account = Column(String, nullable=False, default='')
    total = Column(Double, nullable=False, default=0.0)
    notes = Column(String, nullable=False, default='')
    created_at = Column(DateTime, default=datetime.now())  # Дата создания
    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now()
    )  # Дата обновления


class ChequeDetail(Base):
    __tablename__ = 'cheque_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cheque_id = Column(Integer, ForeignKey('cheques.id'), nullable=True)
    name = Column(String, nullable=False)  # Наименование товара или услуги
    price = Column(Float, nullable=False)  # Цена
    quantity = Column(Float, nullable=False, default=1.0)  # Количество
    total = Column(Float, nullable=False)  # Общая сумма
    created_at = Column(DateTime, default=datetime.now())  # Дата создания
    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now()
    )  # Дата обновления
