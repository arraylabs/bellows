import enum

import bellows.types as t


class Status(t.uint8_t, enum.Enum):
    SUCCESS = 0x00  # Operation was successful.
    FAILURE = 0x01  # Operation was not successful
    NOT_AUTHORIZED = 0x7e  # The sender of the command does not have
    RESERVED_FIELD_NOT_ZERO = 0x7f  # A reserved field/subfield/bit contains a
    MALFORMED_COMMAND = 0x80  # The command appears to contain the wrong
    UNSUP_CLUSTER_COMMAND = 0x81  # The specified cluster command is not
    UNSUP_GENERAL_COMMAND = 0x82  # The specified general ZCL command is not
    UNSUP_MANUF_CLUSTER_COMMAND = 0x83  # A manufacturer specific unicast,
    UNSUP_MANUF_GENERAL_COMMAND = 0x84  # A manufacturer specific unicast, ZCL
    INVALID_FIELD = 0x85  # At least one field of the command contains an
    UNSUPPORTED_ATTRIBUTE = 0x86  # The specified attribute does not exist on
    INVALID_VALUE = 0x87  # Out of range error, or set to a reserved value.
    READ_ONLY = 0x88  # Attempt to write a read only attribute.
    INSUFFICIENT_SPACE = 0x89  # An operation (e.g. an attempt to create an
    DUPLICATE_EXISTS = 0x8a  # An attempt to create an entry in a table failed
    NOT_FOUND = 0x8b  # The requested information (e.g. table entry)
    UNREPORTABLE_ATTRIBUTE = 0x8c  # Periodic reports cannot be issued for this
    INVALID_DATA_TYPE = 0x8d  # The data type given for an attribute is
    INVALID_SELECTOR = 0x8e  # The selector for an attribute is incorrect.
    WRITE_ONLY = 0x8f  # A request has been made to read an attribute
    INCONSISTENT_STARTUP_STATE = 0x90  # Setting the requested values would put
    DEFINED_OUT_OF_BAND = 0x91  # An attempt has been made to write an
    HARDWARE_FAILURE = 0xc0  # An operation was unsuccessful due to a
    SOFTWARE_FAILURE = 0xc1  # An operation was unsuccessful due to a
    CALIBRATION_ERROR = 0xc2  # An error occurred during calibration.


class Analog:
    pass


class Discrete:
    pass


DATA_TYPES = {
    0x00: ('No data', None, None),
    0x08: ('General', t.fixed_list(1, t.uint8_t), Discrete),
    0x09: ('General', t.fixed_list(2, t.uint8_t), Discrete),
    0x0a: ('General', t.fixed_list(3, t.uint8_t), Discrete),
    0x0b: ('General', t.fixed_list(4, t.uint8_t), Discrete),
    0x0c: ('General', t.fixed_list(5, t.uint8_t), Discrete),
    0x0d: ('General', t.fixed_list(6, t.uint8_t), Discrete),
    0x0e: ('General', t.fixed_list(7, t.uint8_t), Discrete),
    0x0f: ('General', t.fixed_list(8, t.uint8_t), Discrete),
    0x10: ('Boolean', t.Bool, Discrete),
    0x18: ('Bitmap', t.uint8_t, Discrete),
    0x19: ('Bitmap', t.uint16_t, Discrete),
    0x1a: ('Bitmap', t.uint24_t, Discrete),
    0x1b: ('Bitmap', t.uint32_t, Discrete),
    0x1c: ('Bitmap', t.uint40_t, Discrete),
    0x1d: ('Bitmap', t.uint48_t, Discrete),
    0x1e: ('Bitmap', t.uint56_t, Discrete),
    0x1f: ('Bitmap', t.uint64_t, Discrete),
    0x20: ('Unsigned Integer', t.uint8_t, Analog),
    0x21: ('Unsigned Integer', t.uint16_t, Analog),
    0x22: ('Unsigned Integer', t.uint24_t, Analog),
    0x23: ('Unsigned Integer', t.uint32_t, Analog),
    0x24: ('Unsigned Integer', t.uint40_t, Analog),
    0x25: ('Unsigned Integer', t.uint48_t, Analog),
    0x26: ('Unsigned Integer', t.uint56_t, Analog),
    0x27: ('Unsigned Integer', t.uint64_t, Analog),
    0x28: ('Signed Integer', t.int8s, Analog),
    0x29: ('Signed Integer', t.int16s, Analog),
    0x2a: ('Signed Integer', t.int24s, Analog),
    0x2b: ('Signed Integer', t.int32s, Analog),
    0x2c: ('Signed Integer', t.int40s, Analog),
    0x2d: ('Signed Integer', t.int48s, Analog),
    0x2e: ('Signed Integer', t.int56s, Analog),
    0x2f: ('Signed Integer', t.int64s, Analog),
    0x30: ('Enumeration', t.uint8_t, Discrete),
    0x31: ('Enumeration', t.uint16_t, Discrete),
    # 0x38: ('Floating point', t.Half, Analog),
    0x39: ('Floating point', t.Single, Analog),
    0x3a: ('Floating point', t.Double, Analog),
    0x41: ('Octet string', t.LVBytes, Discrete),
    0x42: ('Character string', t.LVBytes, Discrete),
    # 0x43: ('Long octet string', ),
    # 0x44: ('Long character string', ),
    # 0x48: ('Array', ),
    # 0x4c: ('Structure', ),
    # 0x50: ('Set', ),
    # 0x51: ('Bag', ),
    0xe0: ('Time of day', t.uint32_t, Analog),
    0xe1: ('Date', t.uint32_t, Analog),
    0xe2: ('UTCTime', t.uint32_t, Analog),
    0xe8: ('Cluster ID', t.uint16_t, Discrete),
    0xe9: ('Attribute ID', t.uint16_t, Discrete),
    0xea: ('BACNet OID', t.uint32_t, Discrete),
    0xf0: ('IEEE address', t.EmberEUI64, Discrete),
    0xf1: ('128-bit security key', t.fixed_list(16, t.uint16_t), Discrete),
    0xff: ('Unknown', None, None),
}

DATA_TYPE_IDX = {
    t: tidx
    for tidx, (tname, t, ad) in DATA_TYPES.items()
    if ad is Analog
}
DATA_TYPE_IDX[t.uint32_t] = 0x23
DATA_TYPE_IDX[t.EmberEUI64] = 0xf0
DATA_TYPE_IDX[t.Bool] = 0x10


class TypeValue():
    def serialize(self):
        return self.type.to_bytes(1, 'little') + self.value.serialize()

    @classmethod
    def deserialize(cls, data):
        self = cls()
        self.type, data = data[0], data[1:]
        actual_type = DATA_TYPES[self.type][1]
        self.value, data = actual_type.deserialize(data)
        return self, data


class ReadAttributeRecord():
    @classmethod
    def deserialize(cls, data):
        r = cls()
        r.attrid, data = int.from_bytes(data[:2], 'little'), data[2:]
        r.status, data = data[0], data[1:]
        if r.status == 0:
            r.value, data = TypeValue.deserialize(data)

        return r, data

    def serialize(self):
        r = t.uint16_t(self.attrid).serialize()
        r += t.uint8_t(self.status).serialize()
        if self.status == 0:
            r += self.value.serialize()

        return r

    def __repr__(self):
        r = '<ReadAttributeRecord attrid=%s status=%s' % (self.attrid, self.status)
        if self.status == 0:
            r += ' value=%s' % (self.value.value, )
        r += '>'
        return r


class Attribute(t.EzspStruct):
    _fields = [
        ('attrid', t.uint16_t),
        ('value', TypeValue),
    ]


class WriteAttributesStatusRecord(t.EzspStruct):
    _fields = [
        ('status', t.uint8_t),
        ('attrid', t.uint16_t),
    ]


class AttributeReportingConfig:
    def serialize(self):
        r = int.to_bytes(self.direction, 1, 'little')
        r += int.to_bytes(self.attrid, 2, 'little')
        if self.direction:
            r += int.to_bytes(self.timeout, 2, 'little')
        else:
            r += (
                int.to_bytes(self.datatype, 1, 'little') +
                int.to_bytes(self.min_interval, 2, 'little') +
                int.to_bytes(self.max_interval, 2, 'little')
            )
            datatype = DATA_TYPES.get(self.datatype, None)
            if datatype and datatype[2] is Analog:
                datatype = datatype[1]
                r += datatype(self.reportable_change).serialize()
        return r

    @classmethod
    def deserialize(cls, data):
        self = cls()
        self.direction, data = t.Bool.deserialize(data)
        self.attrid, data = t.uint16_t.deserialize(data)
        if self.direction:
            # Requesting things to be received by me
            self.timeout, data = t.uint16_t.deserialize(data)
        else:
            # Notifying that I will report things to you
            self.datatype, data = t.uint8_t.deserialize(data)
            self.min_interval, data = t.uint16_t.deserialize(data)
            self.max_interval, data = t.uint16_t.deserialize(data)
            datatype = DATA_TYPES[self.datatype]
            if datatype[2] is Analog:
                self.reportable_change, data = datatype[1].deserialize(data)

        return self, data


class ConfigureReportingResponseRecord(t.EzspStruct):
    _fields = [
        ('status', t.uint8_t),
        ('direction', t.uint8_t),
        ('attrid', t.uint16_t),
    ]


class ReadReportingConfigRecord(t.EzspStruct):
    _fields = [
        ('direction', t.uint8_t),
        ('attrid', t.uint16_t),
    ]


class DiscoverAttributesResponseRecord(t.EzspStruct):
    _fields = [
        ('attrid', t.uint16_t),
        ('datatype', t.uint8_t),
    ]


COMMANDS = {
    # id: (name, params, is_response)
    0x00: ('Read attributes', (t.List(t.uint16_t), ), False),
    0x01: ('Read attributes response', (t.List(ReadAttributeRecord), ), True),
    0x02: ('Write attributes', (t.List(Attribute), ), False),
    0x03: ('Write attributes undivided', (t.List(Attribute), ), False),
    0x04: ('Write attributes response', (t.List(WriteAttributesStatusRecord), ), True),
    0x05: ('Write attributes no response', (t.List(Attribute), ), False),
    0x06: ('Configure reporting', (t.List(AttributeReportingConfig), ), False),
    0x07: ('Configure reporting response', (t.List(ConfigureReportingResponseRecord), ), True),
    0x08: ('Read reporting configuration', (t.List(ReadReportingConfigRecord), ), False),
    0x09: ('Read reporting configuration response', (t.List(AttributeReportingConfig), ), True),
    0x0a: ('Report attributes', (t.List(Attribute), ), False),
    0x0b: ('Default response', (t.uint8_t, Status), True),
    0x0c: ('Discover attributes', (t.uint16_t, t.uint8_t), False),
    0x0d: ('Discover attributes response', (t.List(DiscoverAttributesResponseRecord), ), True),
    # 0x0e: ('Read attributes structured', (, ), False),
    # 0x0f: ('Write attributes structured', (, ), False),
    # 0x10: ('Write attributes structured response', (, ), True),
}
