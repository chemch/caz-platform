from marshmallow import post_load, fields

from .alert import Alert, AlertSchema
from .alert_type import AlertType


class Detection(Alert):
    def __init__(self, description, indicator):
        super(Detection, self).__init__(description, AlertType.DETECTION)
        self.indicator = indicator

    def __repr__(self):
        return '<Detection(name={self.description!r})>'.format(self=self)


class DetectionSchema(AlertSchema):
    indicator = fields.String(required=True)

    @post_load
    def make_detection(self, data):
        return Detection(**data)