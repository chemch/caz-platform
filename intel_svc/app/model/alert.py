import datetime as dt

from marshmallow import Schema, fields


class Alert(object):
    def __init__(self, description, risk_level, type):
        self.description = description
        self.risk_level = risk_level
        self.created_at = dt.datetime.now()
        self.type = type

    def __repr__(self):
        return '<Alert(name={self.description!r})>'.format(self=self)


class AlertSchema(Schema):
    description = fields.Str()
    risk_level = fields.Integer()
    created_at = fields.Date()
    type = fields.Str()