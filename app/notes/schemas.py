from marshmallow import Schema, fields, validate

class NoteSchema(Schema):
    """A class to decribe the notes schema"""
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=3, max=80))
    content = fields.String(required=True, validate=validate.Length(min=3, max=500))
    user_id = fields.Integer(dump_only=True)
    date_created = fields.Date(dump_only=True)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)