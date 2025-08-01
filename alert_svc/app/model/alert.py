import datetime as dt

from marshmallow import Schema, fields


class Alert(object):
    def __init__(self, description, type):
        self.description = description
        self.created_at = dt.datetime.now()
        self.type = type

    def __repr__(self):
        return '<Alert(name={self.description!r})>'.format(self=self)


class AlertSchema(Schema):
    description = fields.Str()
    created_at = fields.Date()
    type = fields.Str()