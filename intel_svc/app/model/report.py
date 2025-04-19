from marshmallow import post_load, fields

from .intel import Intel, IntelSchema
from .intel_type import IntelType


class Report(Intel):
    def __init__(self, name, description, threat, confidence, verdict, severity, source, indicator_count, publish_date):
        super(Report, self).__init__(description, threat, confidence, verdict, severity, IntelType.REPORT, source)
        self.name = name
        self.indicator_count = indicator_count
        self.publish_date = publish_date

    def __repr__(self):
        return '<Report(name={self.name!r})>'.format(self=self)


class ReportSchema(IntelSchema):
    name = fields.Str()
    origin = fields.Str()
    indicator_count = fields.Integer()
    publish_date = fields.Date()

    @post_load
    def make_report(self, data):
        return Report(**data)