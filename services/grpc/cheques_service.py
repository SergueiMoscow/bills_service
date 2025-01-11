import logging
from typing import Optional, List
from datetime import datetime

import grpc
import pydantic
from google.protobuf import timestamp_pb2
from google.protobuf.internal.well_known_types import Timestamp

from db.connector import AsyncSession
from db.models import Cheque, ChequeDetail
from generated.cheques_service import cheques_service_pb2_grpc, cheques_service_pb2
from repository.cheque_detail_repository import get_cheque_details

from repository.get_cheques_repository import get_cheques
from schemas.cheque_schemas import ChequeFilterSchema, ChequeDetailsFilterSchema
from settings import ACCESS_TOKEN
# from generated.cheques_service.cheques_service_pb2 import Cheque as ProtoCheque
# from generated.cheques_service.cheques_service_pb2 import ChequeDetail as ProtoChequeDetail
import generated.cheques_service.cheques_service_pb2 as pb2


logger = logging.getLogger(__name__)

class ChequesService(cheques_service_pb2_grpc.ChequeServiceServicer):

    def __init__(self):
        self.request = None

    async def GetCheques(
        self,
        request,
        context,
    ):
        self.request = request

        if request.token != ACCESS_TOKEN:
            logger.error('Received wrong token')
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('Invalid token')
            return cheques_service_pb2.GetChequesResponse()

        try:
            filters = self._convert_request_to_filter()
        except Exception as e:
            logger.error(f'Error parsing filters: {e}')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid filter parameters')
            return cheques_service_pb2.GetChequesResponse()

        try:
            async with AsyncSession() as session:
                cheques = await get_cheques(session, filters)
        except Exception as e:
            logger.error(f'Error fetching cheques: {e}')
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Internal server error')
            return cheques_service_pb2.GetChequesResponse()

        response = self._convert_cheques_to_response(cheques)
        return response

    async def GetChequeDetails(
            self,
            request,
            context,
    ):
        self.request = request

        if request.token != ACCESS_TOKEN:
            logger.error('Received wrong token for GetChequeDetails')
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('Invalid token')
            return cheques_service_pb2.GetChequeDetailsResponse()

        try:
            filters = self._convert_request_to_details_filter()
        except pydantic.ValidationError as e:
            logger.error(f'Validation Error in filters: {e}')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid filter parameters for details')
            return cheques_service_pb2.GetChequeDetailsResponse()
        except Exception as e:
            logger.error(f'Error parsing details filters: {e}')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid filter parameters for details')
            return cheques_service_pb2.GetChequeDetailsResponse()

        async with AsyncSession() as session:
            try:
                cheque_details = await get_cheque_details(session, filters)
            except Exception as e:
                logger.error(f'Error fetching cheque details: {e}')
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details('Internal server error while fetching details')
                return cheques_service_pb2.GetChequeDetailsResponse()

            response = self._convert_cheque_details_to_response(cheque_details)
        return response

    def _proto_timestamp_to_datetime(self, proto_ts) -> Optional[datetime]:
        if proto_ts is None:
            return None
        return proto_ts.ToDatetime()

    def _convert_request_to_filter(self) -> ChequeFilterSchema:
        filter_pb = self.request.filter

        start_date = self._proto_timestamp_to_datetime(filter_pb.start_date)
        end_date = self._proto_timestamp_to_datetime(filter_pb.end_date)

        return ChequeFilterSchema(
            start_date=start_date,  # self._proto_timestamp_to_datetime(filter_pb.start_date),
            end_date=end_date,  # self._proto_timestamp_to_datetime(filter_pb.end_date),
            seller=filter_pb.seller if filter_pb.seller else None,
            notes=filter_pb.notes if filter_pb.notes else None,
            category=filter_pb.category if filter_pb.category else None,
            total_op=filter_pb.total_op if filter_pb.total_op else None,
            total_value=filter_pb.total_value if filter_pb.total_value else None,
            search=filter_pb.search if filter_pb.search else None,
        )

    def _datetime_to_proto_timestamp(self, dt: Optional[datetime]) -> Optional[Timestamp]:
        if dt is None:
            return None
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(dt)
        return timestamp

    def _convert_cheques_to_response(self, cheques: List[Cheque]):
        response = cheques_service_pb2.GetChequesResponse()
        for cheque in cheques:
            proto_cheque = pb2.Cheque(
                id=cheque.id,
                file_name=cheque.file_name,
                purchase_date=self._datetime_to_proto_timestamp(cheque.purchase_date),
                user=cheque.user,
                seller=cheque.seller,
                account=cheque.account,
                total=cheque.total,
                notes=cheque.notes,
                created_at=self._datetime_to_proto_timestamp(cheque.created_at),
                updated_at=self._datetime_to_proto_timestamp(cheque.updated_at),
            )
            response.cheques.append(proto_cheque)
        return response

    def _convert_request_to_details_filter(self) -> ChequeDetailsFilterSchema:
        filter_pb = self.request.filter

        start_date = self._proto_timestamp_to_datetime(filter_pb.start_date)
        end_date = self._proto_timestamp_to_datetime(filter_pb.end_date)

        return ChequeDetailsFilterSchema(
            start_date=start_date,
            end_date=end_date,
            seller=filter_pb.seller if filter_pb.seller else None,
            notes=filter_pb.notes if filter_pb.notes else None,
            total_op=filter_pb.total_op if filter_pb.total_op else None,
            total_value=filter_pb.total_value if filter_pb.total_value else None,
            item_name=filter_pb.item_name if hasattr(filter_pb, 'item_name') else None,
            item_price_op=filter_pb.item_price_op if hasattr(filter_pb, 'item_price_op') else None,
            item_price_value=filter_pb.item_price_value if hasattr(filter_pb, 'item_price_value') else None,
            item_total_op=filter_pb.item_total_op if hasattr(filter_pb, 'item_total_op') else None,
            item_total_value=filter_pb.item_total_value if hasattr(filter_pb, 'item_total_value') else None,
            search=filter_pb.search if filter_pb.search else None,
        )

    def _convert_cheque_details_to_response(self, cheque_details: List[ChequeDetail]):
        response = cheques_service_pb2.GetChequeDetailsResponse()
        cheque_map = {}

        for detail in cheque_details:
            cheque = detail.cheque
            if cheque.id not in cheque_map:
                cheque_map[cheque.id] = {
                    'cheque': pb2.Cheque(
                        id=cheque.id,
                        file_name=cheque.file_name,
                        purchase_date=self._datetime_to_proto_timestamp(cheque.purchase_date),
                        user=cheque.user,
                        seller=cheque.seller,
                        account=cheque.account,
                        total=cheque.total,
                        notes=cheque.notes,
                        created_at=self._datetime_to_proto_timestamp(cheque.created_at),
                        updated_at=self._datetime_to_proto_timestamp(cheque.updated_at),
                    ),
                    'details': pb2.ChequeDetail(
                        id=detail.id,
                        name=detail.name,
                        price=detail.price,
                        quantity=detail.quantity,
                        total=detail.total,
                        category=detail.category,
                        created_at=self._datetime_to_proto_timestamp(detail.created_at),
                        updated_at=self._datetime_to_proto_timestamp(detail.updated_at),
                    )
                }

        for cheque_id, data in cheque_map.items():
            cheque_with_details = cheques_service_pb2.GetChequeDetailsResponse.ChequeDetailWithHead(
                cheque=data['cheque'],
                detail=data['details']
            )
            response.detail_with_head.append(cheque_with_details)

        return response
