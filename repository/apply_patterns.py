import logging

from sqlalchemy import inspect
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from db.connector import AsyncSession
from db.models import Pattern, ChequeDetail, Cheque

logger = logging.getLogger(__name__)

def get_model_class(model_name):
    """Функция для получения класса модели по её имени."""
    return {
        'Cheque': Cheque,
        'ChequeDetail': ChequeDetail,
    }.get(model_name)

async def apply_patterns(session: AsyncSession, model_object: Cheque | ChequeDetail):
    """Функция для применения всех паттернов к переданному объекту."""
    model_object_name = model_object.__class__.__name__
    modified_objects = []

    # Используем конструкцию select вместо query
    try:
        stmt = select(Pattern).where(Pattern.model_in == model_object_name)
        result = await session.execute(stmt)
        patterns = result.scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при выполнении запроса паттернов: {e}")
        return

    for pattern in patterns:
        model_out_cls = get_model_class(pattern.model_out)

        if not model_out_cls:
            logger.error(f"Неизвестная модель: {pattern.model_out}")
            continue  # Пропускаем паттерны с неизвестными выходными моделями

        try:
            field_in_value = getattr(model_object, pattern.field_in)
        except AttributeError:
            logger.error(f"Модель {model_object_name} не имеет поля {pattern.field_in}")
            continue  # Пропускаем паттерны с неверным полем входа

        # Проверяем условие паттерна (LIKE %include%)
        if isinstance(field_in_value, str) and pattern.include in field_in_value:
            if pattern.model_out == model_object_name:
                # Обновляем поле в самом объекте
                try:
                    setattr(model_object, pattern.field_out, pattern.value_out)
                    logger.info(
                        f"Обновлено поле {pattern.field_out} объекта {model_object}({model_object.id}): {pattern.value_out}"
                    )
                    modified_objects.append(model_object)
                except AttributeError:
                    logger.error(f"Модель {model_object_name} не имеет поля {pattern.field_out}")
            else:
                # Обрабатываем случаи, когда model_out отличается от model_in
                if pattern.model_in == 'Cheque' and pattern.model_out == 'ChequeDetail':
                    if hasattr(model_object, 'details'):
                        for detail in model_object.details:
                            try:
                                setattr(detail, pattern.field_out, pattern.value_out)
                                logger.info(f"Обновлено поле {pattern.field_out} ChequeDetail {detail.id}")
                                modified_objects.append(detail)
                            except AttributeError:
                                logger.error(f"Модель ChequeDetail не имеет поля {pattern.field_out}")
                    else:
                        logger.error(f"Объект Cheque не имеет атрибута 'details'")
                else:
                    logger.warning(f"Не реализована обработка для model_out={pattern.model_out}")

    try:
        for modified_object in modified_objects:
            obj_state = inspect(modified_object)
            if obj_state.session is None:
                session.add(modified_object)
        await session.flush()
        logger.info("Изменения (pattern) успешно сохранены в базе данных.")
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Ошибка (pattern) при сохранении изменений: {e}")
