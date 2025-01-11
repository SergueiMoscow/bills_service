from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChequeFilter(_message.Message):
    __slots__ = ("start_date", "end_date", "seller", "notes", "category", "total_op", "total_value", "search")
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    SELLER_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_OP_FIELD_NUMBER: _ClassVar[int]
    TOTAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    start_date: _timestamp_pb2.Timestamp
    end_date: _timestamp_pb2.Timestamp
    seller: str
    notes: str
    category: str
    total_op: str
    total_value: float
    search: str
    def __init__(self, start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., seller: _Optional[str] = ..., notes: _Optional[str] = ..., category: _Optional[str] = ..., total_op: _Optional[str] = ..., total_value: _Optional[float] = ..., search: _Optional[str] = ...) -> None: ...

class Cheque(_message.Message):
    __slots__ = ("id", "file_name", "purchase_date", "user", "seller", "account", "total", "notes", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_DATE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    SELLER_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    file_name: str
    purchase_date: _timestamp_pb2.Timestamp
    user: str
    seller: str
    account: str
    total: float
    notes: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., file_name: _Optional[str] = ..., purchase_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., user: _Optional[str] = ..., seller: _Optional[str] = ..., account: _Optional[str] = ..., total: _Optional[float] = ..., notes: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ChequeDetail(_message.Message):
    __slots__ = ("id", "name", "price", "quantity", "total", "category", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    price: float
    quantity: float
    total: float
    category: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., price: _Optional[float] = ..., quantity: _Optional[float] = ..., total: _Optional[float] = ..., category: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetChequesRequest(_message.Message):
    __slots__ = ("filter", "token")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    filter: ChequeFilter
    token: str
    def __init__(self, filter: _Optional[_Union[ChequeFilter, _Mapping]] = ..., token: _Optional[str] = ...) -> None: ...

class GetChequesResponse(_message.Message):
    __slots__ = ("cheques",)
    CHEQUES_FIELD_NUMBER: _ClassVar[int]
    cheques: _containers.RepeatedCompositeFieldContainer[Cheque]
    def __init__(self, cheques: _Optional[_Iterable[_Union[Cheque, _Mapping]]] = ...) -> None: ...

class ChequeDetailsFilter(_message.Message):
    __slots__ = ("start_date", "end_date", "seller", "notes", "total_op", "total_value", "item_name", "item_price_op", "item_price_value", "item_total_op", "item_total_value", "search")
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    SELLER_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_OP_FIELD_NUMBER: _ClassVar[int]
    TOTAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    ITEM_NAME_FIELD_NUMBER: _ClassVar[int]
    ITEM_PRICE_OP_FIELD_NUMBER: _ClassVar[int]
    ITEM_PRICE_VALUE_FIELD_NUMBER: _ClassVar[int]
    ITEM_TOTAL_OP_FIELD_NUMBER: _ClassVar[int]
    ITEM_TOTAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    start_date: _timestamp_pb2.Timestamp
    end_date: _timestamp_pb2.Timestamp
    seller: str
    notes: str
    total_op: str
    total_value: float
    item_name: str
    item_price_op: str
    item_price_value: float
    item_total_op: str
    item_total_value: float
    search: str
    def __init__(self, start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., seller: _Optional[str] = ..., notes: _Optional[str] = ..., total_op: _Optional[str] = ..., total_value: _Optional[float] = ..., item_name: _Optional[str] = ..., item_price_op: _Optional[str] = ..., item_price_value: _Optional[float] = ..., item_total_op: _Optional[str] = ..., item_total_value: _Optional[float] = ..., search: _Optional[str] = ...) -> None: ...

class GetChequeDetailsRequest(_message.Message):
    __slots__ = ("filter", "token")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    filter: ChequeDetailsFilter
    token: str
    def __init__(self, filter: _Optional[_Union[ChequeDetailsFilter, _Mapping]] = ..., token: _Optional[str] = ...) -> None: ...

class GetChequeDetailsResponse(_message.Message):
    __slots__ = ("detail_with_head",)
    class ChequeDetailWithHead(_message.Message):
        __slots__ = ("cheque", "detail")
        CHEQUE_FIELD_NUMBER: _ClassVar[int]
        DETAIL_FIELD_NUMBER: _ClassVar[int]
        cheque: Cheque
        detail: ChequeDetail
        def __init__(self, cheque: _Optional[_Union[Cheque, _Mapping]] = ..., detail: _Optional[_Union[ChequeDetail, _Mapping]] = ...) -> None: ...
    DETAIL_WITH_HEAD_FIELD_NUMBER: _ClassVar[int]
    detail_with_head: _containers.RepeatedCompositeFieldContainer[GetChequeDetailsResponse.ChequeDetailWithHead]
    def __init__(self, detail_with_head: _Optional[_Iterable[_Union[GetChequeDetailsResponse.ChequeDetailWithHead, _Mapping]]] = ...) -> None: ...
