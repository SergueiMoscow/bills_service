from pydantic import BaseModel, Field, validator, field_validator
from typing import Optional
from datetime import datetime

class ChequeFilter(BaseModel):
    start_date: Optional[datetime] = Field(None, description="Начальная дата для фильтрации по покупке")
    end_date: Optional[datetime] = Field(None, description="Конечная дата для фильтрации по покупке")
    seller: Optional[str] = Field(None, description="Продавец для фильтрации")
    notes: Optional[str] = Field(None, description="Заметки для фильтрации")
    category: Optional[str] = Field(None, description="Категория для фильтрации")
    total_op: Optional[str] = Field(None, description="Операция для фильтрации по общей сумме")
    total_value: Optional[float] = Field(None, description="Значение для фильтрации по общей сумме")

    @field_validator('total_op')
    def validate_total_op(cls, v):
        allowed_ops = {'<', '<=', '=', '>', '>='}
        if v is not None and v not in allowed_ops:
            raise ValueError(f"Invalid total_op. Allowed values are {allowed_ops}")
        return v


from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class ChequeDetailsFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    seller: Optional[str] = None
    notes: Optional[str] = None
    total_op: Optional[constr(pattern=r'^([<>])?=?$')] = None  # Операторы сравнения
    total_value: Optional[float] = None
    item_name: Optional[str] = None
    item_price_op: Optional[constr(pattern=r'^([<>])?=?$')] = None  # Операторы сравнения
    item_price_value: Optional[float] = None
    item_total_op: Optional[constr(pattern=r'^([<>])?=?$')] = None  # Операторы сравнения
    item_total_value: Optional[float] = None