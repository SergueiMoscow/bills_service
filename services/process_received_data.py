from db.connector import AsyncSession
from services.extract_data import ExtractData
from services.pdf_convert import extract_text_from_pdf
from services.cheque_api_service import get_cheque_from_api_service
from repository.cheque_repository import save_cheque_from_json


async def process_received_data(request, file_path) -> str:

    async with AsyncSession() as session:
        if request.filename.endswith('.txt'):
            # Если это текстовый файл, получаем чек через API и сохраняем
            qrraw = request.description  # строка с параметрами чека
            json_data = await get_cheque_from_api_service(qrraw)
            notes = qrraw  # текст - параметры запроса чека для API, пишем в notes

        elif request.filename.endswith('.pdf'):
            # Если это PDF, извлекаем текст
            extracted_text = extract_text_from_pdf(file_path)

            # Обработка извлеченного текста
            extractor = ExtractData(extracted_text)
            extracted_data = extractor.process()  # Предполагаем, что метод process возвращает нужные данные

            items = [{
                "name": extracted_data['operation_type'],
                "price": extracted_data['amount'],
                "quantity": 1,
                "sum": extracted_data['amount']
            }]

            # Если есть комиссия, добавляем её как второй item
            if extracted_data['commission'] > 0:
                items.append({
                    "name": "Комиссия",
                    "price": extracted_data['commission'],
                    "quantity": 1,
                    "sum": extracted_data['commission']
                })

            # Сохранение данных в базу данных
            json_data = {
                "data": {
                    "json": {
                        "code": 1,  # Добавьте остальные необходимые ключи, если нужно
                        "operationType": extracted_data['operation_type'],
                        "totalSum": extracted_data['amount'] * 100,
                        "dateTime": extracted_data['date'],
                        "user": extracted_data['recipient'],
                        "retailPlace": request.description,
                        "items": items  # Заполните, если есть информация о товарах
                    }
                }
            }
            notes = file_path
        else:
            raise ValueError('Unknown file extension')

        result = await save_cheque_from_json(
            session=session,
            json_data=json_data,
            file_name=notes,
            user=request.username
        )
        await session.commit()
    return result
