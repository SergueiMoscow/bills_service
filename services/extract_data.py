import re
from datetime import datetime
from typing import Optional


class ExtractData:
    MONTHS_RU = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12
    }
    def __init__(self, raw_text):
        self.raw_text = raw_text

    def _extract_amount(self)-> float | None:
        patterns = [
            r'Сумма в валюте операции²\s*\n\s*[\d\s.,]+₽\s+([\d\s.,]+₽)',
            r'Сумма (?:операции|перевода|платежа)\s+([\d\s.,]+₽)',
            r'Сумма ([\d\s.,]+i)'
        ]
        for pattern in patterns:
            match = re.search(pattern, self.raw_text, re.MULTILINE)
            if match:
                # Извлекаем найденную сумму
                amount = match.group(1)
                # Очищаем сумму от пробелов и символа ₽
                # amount_clean = amount.replace('₽', '').replace(' ', '').replace(',', '.')
                amount_clean = re.sub(r'[₽i\s]', '', amount)
                return float(amount_clean)
        return None

    def _extract_date(self) -> Optional[datetime]:
        date_time_patterns = [
            # 1 января 2005 в 01:01
            r'(\d{1,2}) (\w+) (\d{4}) в (\d{1,2}):(\d{2})'
        ]
        for date_time_pattern in date_time_patterns:
            matches = re.findall(date_time_pattern, self.raw_text)
            if matches:
                day, month_ru, year, hour, minutes = matches[-1]
                month = self.MONTHS_RU.get(month_ru.lower())
                if month:
                    try:
                        return datetime(int(year), month, int(day), int(hour), int(minutes))
                    except ValueError:
                        return None

        date_time_patterns = [
            # 01.01.2005 01:01:01
            r'(\d{1,2}).(\d{1,2}).(\d{4}) (\d{1,2}):(\d{2}):(\d{2})'
        ]
        for date_time_pattern in date_time_patterns:
            matches = re.findall(date_time_pattern, self.raw_text)
            if matches:
                day, month, year, hour, minutes, seconds = matches[-1]
                try:
                    return datetime(int(year), int(month), int(day), int(hour), int(minutes), int(seconds))
                except ValueError:
                    return None

        date_patterns = [
            r'(\d{1,2}) (\w+) (\d{4})',
        ]
        for date_pattern in date_patterns:
            matches = re.findall(date_pattern, self.raw_text)
            if matches:
                day, month_ru, year = matches[-1]
                month = self.MONTHS_RU.get(month_ru.lower())
                if month:
                    try:
                        return datetime(int(year), month, int(day))
                    except ValueError:
                        return None
        return None

    def _extract_commission(self) -> float:
        commission_pattern = r'Комиссия\s+([\d,.]+\s?₽)'
        match = re.search(commission_pattern, self.raw_text)
        if match:
            commission_clean = match.group(1).replace('₽', '').replace(' ', '').replace(',', '.')
            try:
                commission = float(commission_clean)
            except ValueError:
                commission = 0.0
        else:
            commission = 0.0
        return commission

    def _extract_recipient(self) -> Optional[str]:
        recipient_patterns = [
            r'ФИО получателя перевода\s+([А-Яа-яёЁ\s.]+)',
            r'Наименование ЮЛ\s+([А-Яа-яёЁ\s"«».]+)',
            r'Магазин\s+([А-Яа-яёЁ\s.,\-]+)',
            r'Описание Статус операции\s+([A-Za-zА-Яа-яёЁ\s]+?)(?:Платёж выполнен|$)',
            r'ФИО получателя\s*:?\s*([А-Яа-яёЁ\s.]+)',
            r'Получатель\s+([А-Яа-яёЁ\s"«».]+)',
        ]
        for pattern in recipient_patterns:
            match = re.search(pattern, self.raw_text, re.MULTILINE)
            if match:
                return match.group(1).strip().split('\n')[0]
        return None

    def _extract_sender(self) -> Optional[str]:
        sender_patterns = [
            r'ФИО отправителя\s+([А-Яа-яёЁ\s.]+)',
            r'Наименование отправителя\s+([А-Яа-яёЁ\s"«».]+)',
            r'Отправитель\s+([А-Яа-яёЁ\s.,\-]+)',
            r'ФИО отправителя\s*:?\s*([А-Яа-яёЁ\s.]+)',
            r'держателем которого является\s+([А-Яа-яёЁ\s.]+)',
            r'Плательщик\s+([А-Яа-яёЁ\s.]+)',
        ]
        for pattern in sender_patterns:
            match = re.search(pattern, self.raw_text, re.MULTILINE)
            if match:
                return match.group(1).strip().split('\n')[0]
        return None

    def _extract_recipient_phone(self) -> Optional[str]:
        phone_patterns = [
            r'Номер телефона получателя\s+(\+7\s?\d{3}\s?\d{3}-\d{2}-\d{2})',
            r'Телефон получателя\s+(\+7\s?\d{3}\s?\d{3}-\d{2}-\d{2})',
            r'Номер телефона\s+(\+7\s?\d{3}\s?\d{3}-\d{2}-\d{2})'
        ]
        for pattern in phone_patterns:
            match = re.search(pattern, self.raw_text)
            if match:
                return match.group(1).strip()
        return None

    def _extract_payment_account(self) -> Optional[str]:
        payment_account_patterns = [
            # Паттерн для "по платежному счету •• 0467"
            r'по платежному счету\s*•+\s*(\d+)',

            # Паттерн для "Счёт списания •• 3343"
            r'Счёт списания\s*•+\s*(\d+)',

            # Паттерн для "Карта отправителя •••• 3343"
            r'Карта отправителя\s*•+\s*(\d+)',

            # Паттерн для просто "•• 3343" или "•••• 3343" при отсутствии описания
            r'•{2,}\s*(\d+)',

            r'Счёт отправителя\s\n?\s*(\S*\s*\d+)'
        ]

        for pattern in payment_account_patterns:
            match = re.search(pattern, self.raw_text, re.MULTILINE | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def _extract_type_operation(self) -> Optional[str]:
        type_operation_patterns = [
            # Обработка строки с 'Тип операции' и возможной датой и временем
            r'Тип операции\s*[:\-]?\s*(?:\d{1,2}\s+\w+\s+\d{4}\s+в\s+\d{2}:\d{2}\s+)?(.+)',
            r'Тип операции\s*\n\s*(?:\d{1,2}\s+\w+\s+\d{4}\s+в\s+\d{2}:\d{2}\s+)?(.+)',
            r'Тип операции\s*[:\-.\s]+\s*(?:\d{1,2}\s+\w+\s+\d{4}\s+в\s+\d{2}:\d{2}\s+)?(.+)',
            r'Тип операции\s*[:\-;]+\s*(?:\d{1,2}\s+\w+\s+\d{4}\s+в\s+\d{2}:\d{2}\s+)?(.+)',
            r'Операция совершена\s*Тип операции\s*[:\-]?\s*(?:\d{1,2}\s+\w+\s+\d{4}\s+в\s+\d{2}:\d{2}\s+)?(.+)',

            # Новый паттерн для обработки формата "Операция\nПеревод по СБП"
            r'Операция\s*\n\s*(.+)',
        ]

        for pattern in type_operation_patterns:
            match = re.search(pattern, self.raw_text, re.MULTILINE | re.IGNORECASE)
            if match:
                operation_type = match.group(1).strip().split('\n')[0]
                return operation_type
        return None

    def process(self):
        data = {}

        # Дата
        extracted_date = self._extract_date()
        if extracted_date:
            format_str = '%Y-%m-%d %H:%M' if extracted_date.hour or extracted_date.minute else '%Y-%m-%d'
            data['date'] = extracted_date.strftime(format_str)
        else:
            data['date'] = None

        # Получатель
        data['recipient'] = self._extract_recipient()

        # Отправитель
        data['sender'] = self._extract_sender()

        # Сумма
        data['amount'] = self._extract_amount()

        # Комиссия
        data['commission'] = self._extract_commission()

        # Номер телефона получателя
        data['recipient_phone'] = self._extract_recipient_phone()

        # Номер телефона получателя
        data['account'] = self._extract_payment_account()

        # Тип операции
        data['operation_type'] = self._extract_type_operation()

        return data
