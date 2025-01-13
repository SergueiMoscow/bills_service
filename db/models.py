from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Double
from datetime import datetime, timezone

from sqlalchemy.orm import relationship

from db.db import Base


_CATEGORY_LENGTH = 20

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

    details = relationship("ChequeDetail", back_populates="cheque")


class ChequeDetail(Base):
    __tablename__ = 'cheque_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cheque_id = Column(Integer, ForeignKey('cheques.id'), nullable=True)
    name = Column(String, nullable=False)  # Наименование товара или услуги
    price = Column(Float, nullable=False)  # Цена
    quantity = Column(Float, nullable=False, default=1.0)  # Количество
    total = Column(Float, nullable=False)  # Общая сумма
    category = Column(String(_CATEGORY_LENGTH), nullable=True, default='')
    created_at = Column(DateTime, default=datetime.now())  # Дата создания
    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now()
    )  # Дата обновления

    cheque = relationship("Cheque", back_populates="details")


# Модель Pattern - для заполнения пустых полей в зависимости от значений других полей
class Pattern(Base):
    __tablename__ = 'patterns'

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_in = Column(String, nullable=False)  # Входная модель, например, 'Cheque'
    field_in = Column(String, nullable=False)  # Входное поле, например, 'seller'
    include = Column(String, nullable=False)  # Значение для поиска, например, 'ORGANIZATION'

    model_out = Column(String, nullable=False)  # Выходная модель, например, 'ChequeDetail'
    field_out = Column(String, nullable=False)  # Выходное поле, например, 'category'
    value_out = Column(String, nullable=False)  # Значение для установки, например, 'Коммунальные услуги'

    def __repr__(self):
        return (f"<Pattern(id={self.id}, model='{self.model}', field_in='{self.field_in}', "
                f"include='{self.include}', field_out='{self.field_out}', value='{self.value}')>")
