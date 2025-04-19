from marshmallow import post_load

from .alert import Alert, AlertSchema
from .alert_type import AlertType


class Incident(Alert):
    def __init__(self, description, risk_level):
        super(Incident, self).__init__(description, risk_level, AlertType.INCIDENT)

    def __repr__(self):
        return '<Incident(name={self.description!r})>'.format(self=self)


class IncidentSchema(AlertSchema):
    @post_load
    def make_incident(self, data):
        return Incident(**data)
