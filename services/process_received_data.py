from db.connector import AsyncSession
from services.extract_data import ExtractData
from services.pdf_convert import extract_text_from_pdf
from services.cheque_api_service import get_cheque_from_api_service
from repository.cheque_repository import save_cheque_from_json


def check_received_json(json_data) -> (int, str):
    """

    :param json_data: - то, что получили из сервиса проверки чеков
    :return: code из json,
            str - если data - строка, то ошибка. В правильном ответе там dict
    """
    if isinstance(json_data.get('data'), str):
        return json_data.get('code'), json_data['data']
    return json_data.get('code'), 'ok'

async def process_received_data(request, file_path) -> str:

    async with AsyncSession() as session:
        if request.filename.endswith('.txt'):
            # Если это текстовый файл, получаем чек через API и сохраняем
            qrraw = request.description  # строка с параметрами чека
            json_data = await get_cheque_from_api_service(qrraw)
            notes = qrraw  # текст - параметры запроса чека для API, пишем в notes
            check_json = check_received_json(json_data)
            if check_json[0] != 1:
                return check_json[1]

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
                        "account": extracted_data['account'],
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
