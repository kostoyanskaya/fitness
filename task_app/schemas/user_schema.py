from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    full_name = fields.Str(required=True)
    gender = fields.Str(required=True)
    birth_date = fields.Date(required=True)
    is_admin = fields.Bool(dump_only=True)


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
