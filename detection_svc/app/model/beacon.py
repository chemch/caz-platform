from marshmallow import post_load, fields

from .detection import Detection, DetectionSchema
from .detection_type import DetectionType


class Beacon(Detection):
    def __init__(self, sensor, indicator, confidence, source_ip, destination_ip, source_port, destination_port, protocol):
        super(Beacon, self).__init__(sensor, indicator, confidence, DetectionType.BEACON)
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.source_port = source_port
        self.destination_port = destination_port
        self.protocol = protocol

    def __repr__(self):
        return '<Beacon(name={self.indicator!r})>'.format(self=self)


class BeaconSchema(DetectionSchema):
    source_ip = fields.String(required=True)
    destination_ip = fields.String(required=True)
    source_port = fields.Integer(required=True)
    destination_port = fields.Integer(required=True)
    protocol = fields.String(required=True)

    @post_load
    def make_beacon(self, data, **kwargs):
        return Beacon(**data)