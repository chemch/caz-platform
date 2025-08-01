from marshmallow import post_load, fields

from .alert import Alert, AlertSchema
from .alert_type import AlertType


class Incident(Alert):
    def __init__(self, description, risk_level):
        super(Incident, self).__init__(description, AlertType.INCIDENT)
        self.risk_level = risk_level

    def __repr__(self):
        return '<Incident(name={self.description!r})>'.format(self=self)


class IncidentSchema(AlertSchema):
    risk_level = fields.Integer()

    @post_load
    def make_incident(self, data):
        return Incident(**data)
