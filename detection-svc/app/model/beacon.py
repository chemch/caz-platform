from marshmallow import post_load

from .detection import Detection, DetectionSchema
from .detection_type import DetectionType


class Beacon(Detection):
    def __init__(self, sensor, indicator, confidence):
        super(Beacon, self).__init__(sensor, indicator, confidence, DetectionType.BEACON)

    def __repr__(self):
        return '<Beacon(name={self.indicator!r})>'.format(self=self)


class BeaconSchema(DetectionSchema):
    @post_load
    def make_beacon(self, data, **kwargs):
        return Beacon(**data)