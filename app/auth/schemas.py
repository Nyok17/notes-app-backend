from marshmallow import Schema, fields, validates_schema, validates, ValidationError
from app.models import User
import re

class UserSchema(Schema):
    """A class to define schema for validation"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    email= fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

    @validates('password')
    def validate_password(self, password):
        """Validate password strength"""
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one number")

        if not re.search(r'[^A-Za-z0-9]', password):
            raise ValidationError("Password must contain at least one special character")

    @validates_schema
    def validate_unique(self, data, **kwargs):
        if User.query.filter_by(email=data['email']).first():
            raise ValidationError("Email already exists")
        
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)