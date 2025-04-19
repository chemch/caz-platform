from marshmallow import post_load

from .alert import Alert, AlertSchema
from .alert_type import AlertType


class Detection(Alert):
    def __init__(self, description, risk_level):
        super(Detection, self).__init__(description, risk_level, AlertType.DETECTION)

    def __repr__(self):
        return '<Detection(name={self.description!r})>'.format(self=self)


class DetectionSchema(AlertSchema):
    @post_load
    def make_detection(self, data):
        return Detection(**data)