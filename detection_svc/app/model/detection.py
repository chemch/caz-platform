import datetime as dt

from marshmallow import Schema, fields


class Detection(object):
    def __init__(self, sensor, indicator, confidence, type):
        self.sensor = sensor
        self.indicator = indicator
        self.confidence = confidence
        self.type = type
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return '<Detection(name={self.indicator!r})>'.format(self=self)


class DetectionSchema(Schema):
    sensor = fields.Str()
    indicator = fields.Str()
    confidence = fields.Float()
    type = fields.Str()
    created_at = fields.Date()