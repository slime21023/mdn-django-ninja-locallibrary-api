from catalog.models import Book, Author, Genre
from typing import Optional
from ninja import ModelSchema, Schema, Field
from datetime import date


class Error(Schema):
    message: str


class BookSchema(ModelSchema):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "summary", "isbn", "genre", "language"]


class AuthorSchema(ModelSchema):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "date_of_birth", "date_of_death"]


class GenreSchema(ModelSchema):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class BookCreateSchema(Schema):
    title: str = Field(..., description="The title of the book", max_length=200)
    summary: str = Field(..., max_length=1000)
    isbn: str = Field(..., max_length=13)
    author_id: Optional[int] = None
    language_id: Optional[int] = None


class BookPatchSchema(BookCreateSchema):
    pass


class AuthorCreateSchema(Schema):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    date_of_birth: Optional[date] = None
    date_of_death: Optional[date] = None


class AuthorPatchSchema(AuthorCreateSchema):
    pass


class GenreCreateSchema(Schema):
    name: str = Field(..., max_length=200)

