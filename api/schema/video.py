from flask_marshmallow import Schema
from marshmallow.fields import Str


class VideoSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["path"]

    path = Str()