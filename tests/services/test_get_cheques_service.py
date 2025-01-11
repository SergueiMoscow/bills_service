import grpc
import pytest
from unittest import mock
from unittest.mock import AsyncMock, MagicMock

from datetime import datetime, timezone
from google.protobuf import timestamp_pb2

from schemas.cheque_schemas import ChequeDetailsFilterSchema
from services.grpc.cheques_service import ChequesService


from generated.cheques_service import cheques_service_pb2
from generated.cheques_service import cheques_service_pb2_grpc
from settings import ACCESS_TOKEN


@pytest.mark.asyncio
async def test_GetChequeDetails_with_valid_token_and_valid_filters(mock_services_grpc_cheque_services_get_cheque_details):
    # Создаем экземпляр сервиса
    service = ChequesService()

    # Создаем фиктивный запрос с правильным токеном и фильтрами
    request = cheques_service_pb2.GetChequeDetailsRequest(
        token=ACCESS_TOKEN,
        filter=cheques_service_pb2.ChequeDetailsFilter(
            start_date=timestamp_pb2.Timestamp(seconds=int(datetime(2023, 1, 1, tzinfo=timezone.utc).timestamp())),
            end_date=timestamp_pb2.Timestamp(seconds=int(datetime(2023, 12, 31, tzinfo=timezone.utc).timestamp())),
            seller="Test Seller",
            notes="Test Notes",
            total_op=">=",
            total_value=100.0,
            item_name="Test Item",
            item_price_op="<",
            item_price_value=50.0,
            item_total_op="=",
            item_total_value=150.0,
            search="Test Search"
        )
    )

    # Задаем возвратную значение для мокированной функции
    mock_services_grpc_cheque_services_get_cheque_details.return_value = [
        # Добавьте здесь объекты ChequeDetail, которые вы ожидаете
    ]
    context = MagicMock()
    response = await service.GetChequeDetails(request, context)

    # Проверяем, что get_cheque_details была вызвана с правильными параметрами
    expected_filters = service._convert_request_to_details_filter()
    mock_services_grpc_cheque_services_get_cheque_details.assert_awaited_once_with(mock.ANY, expected_filters)

    # Проверяем, что контекст не содержит ошибок
    context.set_code.assert_not_called()
    context.set_details.assert_not_called()

    # Дополнительно можно проверить содержимое ответа
    assert isinstance(response, cheques_service_pb2.GetChequeDetailsResponse)
    # Добавьте дополнительные assert'ы для проверки содержимого response


@pytest.mark.asyncio
async def test_GetChequeDetails_with_invalid_token(mock_services_grpc_cheque_services_get_cheque_details):
    service = ChequesService()

    request = cheques_service_pb2.GetChequeDetailsRequest(
        token="INVALID_TOKEN",
        filter=cheques_service_pb2.ChequeDetailsFilter()
    )

    context = MagicMock()

    response = await service.GetChequeDetails(request, context)

    # Убедимся, что get_cheque_details не был вызван
    mock_services_grpc_cheque_services_get_cheque_details.assert_not_called()

    # Проверяем, что контекст установлен на UNAUTHENTICATED
    context.set_code.assert_called_once_with(grpc.StatusCode.UNAUTHENTICATED)
    context.set_details.assert_called_once_with('Invalid token')

    # Проверяем, что ответ пуст
    assert isinstance(response, cheques_service_pb2.GetChequeDetailsResponse)
    assert "Invalid token" in context.set_details.call_args[0]


@pytest.mark.asyncio
async def test_GetChequeDetails_with_invalid_filters(mock_services_grpc_cheque_services_get_cheque_details):
    service = ChequesService()

    request = cheques_service_pb2.GetChequeDetailsRequest(
        token=ACCESS_TOKEN,
        filter=cheques_service_pb2.ChequeDetailsFilter(
            total_op="INVALID_OP"  # Преднамеренно неверный оператор
        )
    )

    context = MagicMock()

    response = await service.GetChequeDetails(request, context)

    # Убедимся, что get_cheque_details не был вызван из-за ошибки в фильтре
    mock_services_grpc_cheque_services_get_cheque_details.assert_not_called()

    # Проверяем, что контекст установлен на INVALID_ARGUMENT
    context.set_code.assert_called_once_with(grpc.StatusCode.INVALID_ARGUMENT)
    context.set_details.assert_called_once_with('Invalid filter parameters for details')

    # Проверяем, что ответ содержит сообщение об ошибке
    assert isinstance(response, cheques_service_pb2.GetChequeDetailsResponse)

    assert "Invalid filter parameters for details" in context.set_details.call_args[0]

