# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: world_amazon.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12world_amazon.proto\":\n\x08\x41Product\x12\n\n\x02id\x18\x01 \x02(\x03\x12\x13\n\x0b\x64\x65scription\x18\x02 \x02(\t\x12\r\n\x05\x63ount\x18\x03 \x02(\x05\"2\n\x0e\x41InitWarehouse\x12\n\n\x02id\x18\x01 \x02(\x05\x12\t\n\x01x\x18\x02 \x02(\x05\x12\t\n\x01y\x18\x03 \x02(\x05\"N\n\x08\x41\x43onnect\x12\x0f\n\x07worldid\x18\x01 \x01(\x03\x12\x1f\n\x06initwh\x18\x02 \x03(\x0b\x32\x0f.AInitWarehouse\x12\x10\n\x08isAmazon\x18\x03 \x02(\x08\"-\n\nAConnected\x12\x0f\n\x07worldid\x18\x01 \x02(\x03\x12\x0e\n\x06result\x18\x02 \x02(\t\"Q\n\x05\x41Pack\x12\r\n\x05whnum\x18\x01 \x02(\x05\x12\x19\n\x06things\x18\x02 \x03(\x0b\x32\t.AProduct\x12\x0e\n\x06shipid\x18\x03 \x02(\x03\x12\x0e\n\x06seqnum\x18\x04 \x02(\x03\")\n\x07\x41Packed\x12\x0e\n\x06shipid\x18\x01 \x02(\x03\x12\x0e\n\x06seqnum\x18\x02 \x02(\x03\")\n\x07\x41Loaded\x12\x0e\n\x06shipid\x18\x01 \x02(\x03\x12\x0e\n\x06seqnum\x18\x02 \x02(\x03\"M\n\x0b\x41PutOnTruck\x12\r\n\x05whnum\x18\x01 \x02(\x05\x12\x0f\n\x07truckid\x18\x02 \x02(\x05\x12\x0e\n\x06shipid\x18\x03 \x02(\x03\x12\x0e\n\x06seqnum\x18\x04 \x02(\x03\"I\n\rAPurchaseMore\x12\r\n\x05whnum\x18\x01 \x02(\x05\x12\x19\n\x06things\x18\x02 \x03(\x0b\x32\t.AProduct\x12\x0e\n\x06seqnum\x18\x03 \x02(\x03\"9\n\x04\x41\x45rr\x12\x0b\n\x03\x65rr\x18\x01 \x02(\t\x12\x14\n\x0coriginseqnum\x18\x02 \x02(\x03\x12\x0e\n\x06seqnum\x18\x03 \x02(\x03\"+\n\x06\x41Query\x12\x11\n\tpackageid\x18\x01 \x02(\x03\x12\x0e\n\x06seqnum\x18\x02 \x02(\x03\"=\n\x08\x41Package\x12\x11\n\tpackageid\x18\x01 \x02(\x03\x12\x0e\n\x06status\x18\x02 \x02(\t\x12\x0e\n\x06seqnum\x18\x03 \x02(\x03\"\xaa\x01\n\tACommands\x12\x1b\n\x03\x62uy\x18\x01 \x03(\x0b\x32\x0e.APurchaseMore\x12\x16\n\x06topack\x18\x02 \x03(\x0b\x32\x06.APack\x12\x1a\n\x04load\x18\x03 \x03(\x0b\x32\x0c.APutOnTruck\x12\x18\n\x07queries\x18\x04 \x03(\x0b\x32\x07.AQuery\x12\x10\n\x08simspeed\x18\x05 \x01(\r\x12\x12\n\ndisconnect\x18\x06 \x01(\x08\x12\x0c\n\x04\x61\x63ks\x18\x07 \x03(\x03\"\xb8\x01\n\nAResponses\x12\x1f\n\x07\x61rrived\x18\x01 \x03(\x0b\x32\x0e.APurchaseMore\x12\x17\n\x05ready\x18\x02 \x03(\x0b\x32\x08.APacked\x12\x18\n\x06loaded\x18\x03 \x03(\x0b\x32\x08.ALoaded\x12\x10\n\x08\x66inished\x18\x04 \x01(\x08\x12\x14\n\x05\x65rror\x18\x05 \x03(\x0b\x32\x05.AErr\x12\x0c\n\x04\x61\x63ks\x18\x06 \x03(\x03\x12 \n\rpackagestatus\x18\x07 \x03(\x0b\x32\t.APackage')



_APRODUCT = DESCRIPTOR.message_types_by_name['AProduct']
_AINITWAREHOUSE = DESCRIPTOR.message_types_by_name['AInitWarehouse']
_ACONNECT = DESCRIPTOR.message_types_by_name['AConnect']
_ACONNECTED = DESCRIPTOR.message_types_by_name['AConnected']
_APACK = DESCRIPTOR.message_types_by_name['APack']
_APACKED = DESCRIPTOR.message_types_by_name['APacked']
_ALOADED = DESCRIPTOR.message_types_by_name['ALoaded']
_APUTONTRUCK = DESCRIPTOR.message_types_by_name['APutOnTruck']
_APURCHASEMORE = DESCRIPTOR.message_types_by_name['APurchaseMore']
_AERR = DESCRIPTOR.message_types_by_name['AErr']
_AQUERY = DESCRIPTOR.message_types_by_name['AQuery']
_APACKAGE = DESCRIPTOR.message_types_by_name['APackage']
_ACOMMANDS = DESCRIPTOR.message_types_by_name['ACommands']
_ARESPONSES = DESCRIPTOR.message_types_by_name['AResponses']
AProduct = _reflection.GeneratedProtocolMessageType('AProduct', (_message.Message,), {
  'DESCRIPTOR' : _APRODUCT,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:AProduct)
  })
_sym_db.RegisterMessage(AProduct)

AInitWarehouse = _reflection.GeneratedProtocolMessageType('AInitWarehouse', (_message.Message,), {
  'DESCRIPTOR' : _AINITWAREHOUSE,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:AInitWarehouse)
  })
_sym_db.RegisterMessage(AInitWarehouse)

AConnect = _reflection.GeneratedProtocolMessageType('AConnect', (_message.Message,), {
  'DESCRIPTOR' : _ACONNECT,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:AConnect)
  })
_sym_db.RegisterMessage(AConnect)

AConnected = _reflection.GeneratedProtocolMessageType('AConnected', (_message.Message,), {
  'DESCRIPTOR' : _ACONNECTED,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:AConnected)
  })
_sym_db.RegisterMessage(AConnected)

APack = _reflection.GeneratedProtocolMessageType('APack', (_message.Message,), {
  'DESCRIPTOR' : _APACK,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:APack)
  })
_sym_db.RegisterMessage(APack)

APacked = _reflection.GeneratedProtocolMessageType('APacked', (_message.Message,), {
  'DESCRIPTOR' : _APACKED,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:APacked)
  })
_sym_db.RegisterMessage(APacked)

ALoaded = _reflection.GeneratedProtocolMessageType('ALoaded', (_message.Message,), {
  'DESCRIPTOR' : _ALOADED,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:ALoaded)
  })
_sym_db.RegisterMessage(ALoaded)

APutOnTruck = _reflection.GeneratedProtocolMessageType('APutOnTruck', (_message.Message,), {
  'DESCRIPTOR' : _APUTONTRUCK,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:APutOnTruck)
  })
_sym_db.RegisterMessage(APutOnTruck)

APurchaseMore = _reflection.GeneratedProtocolMessageType('APurchaseMore', (_message.Message,), {
  'DESCRIPTOR' : _APURCHASEMORE,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:APurchaseMore)
  })
_sym_db.RegisterMessage(APurchaseMore)

AErr = _reflection.GeneratedProtocolMessageType('AErr', (_message.Message,), {
  'DESCRIPTOR' : _AERR,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:AErr)
  })
_sym_db.RegisterMessage(AErr)

AQuery = _reflection.GeneratedProtocolMessageType('AQuery', (_message.Message,), {
  'DESCRIPTOR' : _AQUERY,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:AQuery)
  })
_sym_db.RegisterMessage(AQuery)

APackage = _reflection.GeneratedProtocolMessageType('APackage', (_message.Message,), {
  'DESCRIPTOR' : _APACKAGE,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:APackage)
  })
_sym_db.RegisterMessage(APackage)

ACommands = _reflection.GeneratedProtocolMessageType('ACommands', (_message.Message,), {
  'DESCRIPTOR' : _ACOMMANDS,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:ACommands)
  })
_sym_db.RegisterMessage(ACommands)

AResponses = _reflection.GeneratedProtocolMessageType('AResponses', (_message.Message,), {
  'DESCRIPTOR' : _ARESPONSES,
  '__module__' : 'world_amazon_pb2'
  # @@protoc_insertion_point(class_scope:AResponses)
  })
_sym_db.RegisterMessage(AResponses)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _APRODUCT._serialized_start=22
  _APRODUCT._serialized_end=80
  _AINITWAREHOUSE._serialized_start=82
  _AINITWAREHOUSE._serialized_end=132
  _ACONNECT._serialized_start=134
  _ACONNECT._serialized_end=212
  _ACONNECTED._serialized_start=214
  _ACONNECTED._serialized_end=259
  _APACK._serialized_start=261
  _APACK._serialized_end=342
  _APACKED._serialized_start=344
  _APACKED._serialized_end=385
  _ALOADED._serialized_start=387
  _ALOADED._serialized_end=428
  _APUTONTRUCK._serialized_start=430
  _APUTONTRUCK._serialized_end=507
  _APURCHASEMORE._serialized_start=509
  _APURCHASEMORE._serialized_end=582
  _AERR._serialized_start=584
  _AERR._serialized_end=641
  _AQUERY._serialized_start=643
  _AQUERY._serialized_end=686
  _APACKAGE._serialized_start=688
  _APACKAGE._serialized_end=749
  _ACOMMANDS._serialized_start=752
  _ACOMMANDS._serialized_end=922
  _ARESPONSES._serialized_start=925
  _ARESPONSES._serialized_end=1109
# @@protoc_insertion_point(module_scope)
