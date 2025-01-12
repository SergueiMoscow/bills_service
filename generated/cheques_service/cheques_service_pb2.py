# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: cheques_service.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'cheques_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x63heques_service.proto\x12\x19generated.cheques_service\x1a\x1fgoogle/protobuf/timestamp.proto\"\xd4\x01\n\x0c\x43hequeFilter\x12.\n\nstart_date\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08\x65nd_date\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06seller\x18\x03 \x01(\t\x12\r\n\x05notes\x18\x04 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x05 \x01(\t\x12\x10\n\x08total_op\x18\x06 \x01(\t\x12\x13\n\x0btotal_value\x18\x07 \x01(\x01\x12\x0e\n\x06search\x18\x08 \x01(\t\"\x87\x02\n\x06\x43heque\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x11\n\tfile_name\x18\x02 \x01(\t\x12\x31\n\rpurchase_date\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04user\x18\x04 \x01(\t\x12\x0e\n\x06seller\x18\x05 \x01(\t\x12\x0f\n\x07\x61\x63\x63ount\x18\x06 \x01(\t\x12\r\n\x05total\x18\x07 \x01(\x01\x12\r\n\x05notes\x18\x08 \x01(\t\x12.\n\ncreated_at\x18\t \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\n \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\xca\x01\n\x0c\x43hequeDetail\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05price\x18\x03 \x01(\x01\x12\x10\n\x08quantity\x18\x04 \x01(\x01\x12\r\n\x05total\x18\x05 \x01(\x01\x12\x10\n\x08\x63\x61tegory\x18\x06 \x01(\t\x12.\n\ncreated_at\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"[\n\x11GetChequesRequest\x12\x37\n\x06\x66ilter\x18\x01 \x01(\x0b\x32\'.generated.cheques_service.ChequeFilter\x12\r\n\x05token\x18\x02 \x01(\t\"H\n\x12GetChequesResponse\x12\x32\n\x07\x63heques\x18\x01 \x03(\x0b\x32!.generated.cheques_service.Cheque\"\xbe\x02\n\x13\x43hequeDetailsFilter\x12.\n\nstart_date\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08\x65nd_date\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06seller\x18\x03 \x01(\t\x12\r\n\x05notes\x18\x04 \x01(\t\x12\x10\n\x08total_op\x18\x05 \x01(\t\x12\x13\n\x0btotal_value\x18\x06 \x01(\x01\x12\x11\n\titem_name\x18\x07 \x01(\t\x12\x15\n\ritem_price_op\x18\x08 \x01(\t\x12\x18\n\x10item_price_value\x18\t \x01(\x01\x12\x15\n\ritem_total_op\x18\n \x01(\t\x12\x18\n\x10item_total_value\x18\x0b \x01(\x01\x12\x0e\n\x06search\x18\x0c \x01(\t\"h\n\x17GetChequeDetailsRequest\x12>\n\x06\x66ilter\x18\x01 \x01(\x0b\x32..generated.cheques_service.ChequeDetailsFilter\x12\r\n\x05token\x18\x02 \x01(\t\"\x83\x02\n\x18GetChequeDetailsResponse\x12\x62\n\x10\x64\x65tail_with_head\x18\x01 \x03(\x0b\x32H.generated.cheques_service.GetChequeDetailsResponse.ChequeDetailWithHead\x1a\x82\x01\n\x14\x43hequeDetailWithHead\x12\x31\n\x06\x63heque\x18\x01 \x01(\x0b\x32!.generated.cheques_service.Cheque\x12\x37\n\x06\x64\x65tail\x18\x02 \x01(\x0b\x32\'.generated.cheques_service.ChequeDetail2\xf7\x01\n\rChequeService\x12i\n\nGetCheques\x12,.generated.cheques_service.GetChequesRequest\x1a-.generated.cheques_service.GetChequesResponse\x12{\n\x10GetChequeDetails\x12\x32.generated.cheques_service.GetChequeDetailsRequest\x1a\x33.generated.cheques_service.GetChequeDetailsResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cheques_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CHEQUEFILTER']._serialized_start=86
  _globals['_CHEQUEFILTER']._serialized_end=298
  _globals['_CHEQUE']._serialized_start=301
  _globals['_CHEQUE']._serialized_end=564
  _globals['_CHEQUEDETAIL']._serialized_start=567
  _globals['_CHEQUEDETAIL']._serialized_end=769
  _globals['_GETCHEQUESREQUEST']._serialized_start=771
  _globals['_GETCHEQUESREQUEST']._serialized_end=862
  _globals['_GETCHEQUESRESPONSE']._serialized_start=864
  _globals['_GETCHEQUESRESPONSE']._serialized_end=936
  _globals['_CHEQUEDETAILSFILTER']._serialized_start=939
  _globals['_CHEQUEDETAILSFILTER']._serialized_end=1257
  _globals['_GETCHEQUEDETAILSREQUEST']._serialized_start=1259
  _globals['_GETCHEQUEDETAILSREQUEST']._serialized_end=1363
  _globals['_GETCHEQUEDETAILSRESPONSE']._serialized_start=1366
  _globals['_GETCHEQUEDETAILSRESPONSE']._serialized_end=1625
  _globals['_GETCHEQUEDETAILSRESPONSE_CHEQUEDETAILWITHHEAD']._serialized_start=1495
  _globals['_GETCHEQUEDETAILSRESPONSE_CHEQUEDETAILWITHHEAD']._serialized_end=1625
  _globals['_CHEQUESERVICE']._serialized_start=1628
  _globals['_CHEQUESERVICE']._serialized_end=1875
# @@protoc_insertion_point(module_scope)