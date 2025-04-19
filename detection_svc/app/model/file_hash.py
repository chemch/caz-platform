from marshmallow import fields, post_load

from .detection import Detection, DetectionSchema
from .detection_type import DetectionType


class FileHash(Detection):
    def __init__(self, sensor, indicator, confidence, hash_type, hash_value):
        super(FileHash, self).__init__(sensor, indicator, confidence, DetectionType.FILE_HASH)
        self.hash_type = hash_type
        self.hash_value = hash_value

    def __repr__(self):
        return '<FileHash(name={self.indicator!r})>'.format(self=self)


class FileHashSchema(DetectionSchema):
    hash_type = fields.String(required=True)
    hash_value = fields.String(required=True)
    confidence = fields.Integer(required=True)

    @post_load
    def make_file_hash(self, data, **kwargs):
        return FileHash(**data)
