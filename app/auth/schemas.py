from marshmallow import Schema, fields, validates_schema, ValidationError, validate
from app.models import User

class UserSchema(Schema):
    """A class to define schema for validation"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    email= fields.Email(required=True)
    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.And(
            validate.Length(min=8, error="Password must be at least 8 characters long"),
            validate.Regexp(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])',
                error='Password must include at least one uppercase letter, one lowercase letter, one number, and one special character'
            )
        )
    )


    @validates_schema
    def validate_unique(self, data, **kwargs):
        if User.query.filter_by(email=data['email']).first():
            raise ValidationError("Email already exists")
        
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)