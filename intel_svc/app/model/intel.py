import datetime as dt

from marshmallow import Schema, fields


class Intel(object):
    def __init__(self, description, threat, confidence, verdict, severity, type, source):
        self.description = description
        self.threat = threat
        self.confidence = confidence
        self.verdict = verdict
        self.severity = severity
        self.type = type
        self.source = source
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return '<Intel(name={self.description!r})>'.format(self=self)


class IntelSchema(Schema):
    description = fields.Str()
    created_at = fields.Date()
    type = fields.Str()
    threat = fields.Str()
    origin = fields.Str()
    confidence = fields.Integer()
    verdict = fields.Str()
    severity = fields.Str()
    source = fields.Str()