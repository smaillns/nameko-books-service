import json

from marshmallow import ValidationError
from nameko_sqlalchemy import DatabaseSession
from werkzeug import Response

from books.exceptions import HttpError, NotFound, BadRequest
from books.models import DeclarativeBase, Book, Author
from books.schemas import BookSchema, CreateBookSchema
from datetime import datetime, timezone
from nameko.web.handlers import HttpRequestHandler
from nameko.exceptions import safe_for_serialization


# control formatting of errors returned from the service by overriding response_from_exception()
# more https://nameko.readthedocs.io/en/stable/built_in_extensions.html#http
class HttpEntrypoint(HttpRequestHandler):
    def response_from_exception(self, exc):
        if isinstance(exc, HttpError):
            response = Response(
                json.dumps({
                    'error': exc.error_code,
                    'message': safe_for_serialization(exc),
                }),
                status=exc.status_code,
                mimetype='application/json'
            )
            return response
        return HttpRequestHandler.response_from_exception(self, exc)


http = HttpEntrypoint.decorator


class BooksService:
    name = 'books_service'
    db = DatabaseSession(DeclarativeBase)

    @http('GET', '/books')
    def get_all_books(self, request):
        """Get All Books."""
        books = self.db.query(Book).all()

        return Response(
            BookSchema(many=True).dumps(books),
            mimetype='application/json'
        )

    @http('GET', '/books/<int:book_id>', expected_exceptions=NotFound)
    def get_book(self, request, book_id):
        """Get Book by Id."""
        book = self.db.query(Book).get(book_id)
        if not book:
            raise NotFound('Element not found !')

        return Response(
            BookSchema().dumps(book),
            mimetype='application/json'
        )

    @http('POST', '/books')
    def create_book(self, request):
        """Create a new Book."""
        schema = CreateBookSchema()
        try:
            # use marshmallow schema for validation
            # Note - this may raise `ValueError` for invalid json,
            # or `ValidationError` if data is invalid.
            upload = schema.loads(request.get_data(as_text=True))
        except (ValueError, ValidationError) as exc:
            raise BadRequest("Invalid data: {}".format(exc))

        book = Book(
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            author_id=upload.get('author_id'),
            title=upload.get('title')
        )
        self.db.add(book)
        self.db.commit()
        return Response(
            json.dumps({'id': book.id}),
            mimetype='application/json',
            status=201
        )

    @http('DELETE', '/books/<int:book_id>')
    def delete_book(self, request, book_id):
        """Delete a Book."""
        book = self.db.query(Book).get(book_id)
        if not book:
            raise NotFound('Element not found !')

        self.db.delete(book)
        self.db.commit()
        return 204, 'Ressource deleted successfully'

    @http('PUT', '/books/<int:book_id>')
    def update_book(self, request, book_id):
        """Update a Book."""
        book = self.db.query(Book).get(book_id)
        if not book:
            raise NotFound('Element not found !')

        request_body = json.loads(request.get_data(as_text=True))
        book.updated_at = datetime.now(timezone.utc)
        book.title = request_body.get('title') or book.title
        self.db.commit()
        return 200, 'Element updated successfully'

    @http('POST', '/authors')
    def create_author(self, request):
        """Add new Author."""
        upload = json.loads(request.get_data(as_text=True))
        author = Author(
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            name=upload.get('name'),
            gender=upload.get('gender')
        )
        self.db.add(author)
        self.db.commit()
        return Response(
            json.dumps({'id': author.id}),
            status=201,
            mimetype='application/json'
        )
