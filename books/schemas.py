from marshmallow import Schema, fields


class AuthorSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    gender = fields.Str(required=True)
    created_at = fields.Date()
    updated_at = fields.Date()


class BookSchema(Schema):
    id = fields.Int(required=True)
    created_at = fields.Date()
    updated_at = fields.Date()
    title = fields.Str(required=True)
    author = fields.Nested(AuthorSchema, many=False)


class CreateBookSchema(Schema):
    title = fields.Str(default=None)
    author_id = fields.Int(required=True)
