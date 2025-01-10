import logging
from typing import Optional, List
from datetime import datetime

import grpc
from google.protobuf.internal.well_known_types import Timestamp

from db.connector import AsyncSession
from db.models import Cheque
from generated.cheques_service import cheques_service_pb2_grpc, cheques_service_pb2

from repository.get_cheques_repository import get_cheques
from schemas.cheque_schemas import ChequeFilter
from settings import ACCESS_TOKEN

logger = logging.getLogger(__name__)

class ChequesService(cheques_service_pb2_grpc.ChequeServiceServicer):

    def __init__(self):
        self.request = None

    async def get_cheques(
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
            with AsyncSession() as session:
                cheques = await get_cheques(session, filters)
        except Exception as e:
            logger.error(f'Error fetching cheques: {e}')
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Internal server error')
            return cheques_service_pb2.GetChequesResponse()

        response = self._convert_cheques_to_response(cheques)
        return response

    def _proto_timestamp_to_datetime(self, proto_ts) -> Optional[datetime]:
        if proto_ts is None:
            return None
        return proto_ts.ToDatetime()

    def _convert_request_to_filter(self) -> ChequeFilter:
        filter_pb = self.request.filter

        return ChequeFilter(
            start_date=self._proto_timestamp_to_datetime(filter_pb.start_date),
            end_date=self._proto_timestamp_to_datetime(filter_pb.end_date),
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
        timestamp = Timestamp()
        timestamp.FromDatetime(dt)
        return timestamp

    def _convert_cheques_to_response(self, cheques: List[Cheque]):
        response = cheques_service_pb2.GetChequesResponse()
        for cheque in cheques:
            proto_cheque = cheques_service_pb2.ProtoCheque(
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