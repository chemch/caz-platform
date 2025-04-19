from marshmallow import post_load, fields

from .intel import Intel, IntelSchema
from .intel_type import IntelType


class Indicator(Intel):
    def __init__(self,  description, threat, confidence, verdict, severity, source, id, value ):
        super(Indicator, self).__init__(description, threat, confidence, verdict, severity, IntelType.INDICATOR, source)
        self.id = id
        self.value = value

    def __repr__(self):
        return '<Indicator(name={self.id!r})>'.format(self=self)


class IndicatorSchema(IntelSchema):
    id = fields.Str()
    value = fields.Str()

    @post_load
    def make_indicator(self, data):
        return Indicator(**data)
