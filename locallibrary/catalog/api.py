from ninja import NinjaAPI
from ninja.security import django_auth_superuser
from django.core.exceptions import ObjectDoesNotExist
from catalog.models import Book, Author, Language, Genre
import catalog.schema as schema

api = NinjaAPI()


# The api for general purpose use
@api.get("/books", response=list[schema.BookSchema])
def get_books(request):
    """Returns a list of all books."""
    return Book.objects.all()


@api.get("/books/{id}", response={200: schema.BookSchema, 404: schema.Error})
def get_book_by_id(request, id: int):
    """Returns a book by its id."""
    if not Book.objects.filter(id=id).exists():
        return 404, {"message": "Book NOT_FOUND"}

    return Book.objects.get(id=id)


@api.get("/books/{id}/genre", response={200: schema.GenreSchema, 404: schema.Error})
def get_book_genre(request, id: int):
    """Returns a book by its id."""
    if not Book.objects.filter(id=id).exists():
        return 404, {"message": "Book NOT_FOUND"}
    book = Book.objects.get(id=id)
    return Genre.objects.get(id=book.genre.id)


@api.get("/genres", response=list[schema.GenreSchema])
def get_genres(request):
    """Returns a list of all genres."""
    return Genre.objects.all()


@api.get("/authors", response=list[schema.AuthorSchema])
def get_authors(request):
    """Returns a list of all authors."""
    return Author.objects.all()


@api.get("/authors/{id}", response={200: schema.AuthorSchema, 404: schema.Error})
def get_author_by_id(request, id: int):
    """Returns an author by its id."""
    if not Author.objects.filter(id=id).exists():
        return 404, {"message": "Author NOT_FOUND"}

    return Author.objects.get(id=id)


# The api for superusers only
@api.post(
    "/books",
    response={201: None, 400: schema.Error},
    tags=["admin"],
    auth=django_auth_superuser,
)
def create_book(request, book: schema.BookCreateSchema):
    """Create a new book"""
    try:
        author = (
            Author.objects.get(id=book.author_id)
            if book.author_id is not None
            else None
        )

        language = (
            Language.objects.get(id=book.language_id)
            if book.language_id is not None
            else None
        )

        Book.objects.create(
            title=book.title,
            author=author,
            language=language,
            summary=book.summary,
            isbn=book.isbn,
            genre=book.genre,
        )
        return
    except ObjectDoesNotExist:
        return 400, {"message": "Author or Language NOT_FOUND"}


@api.patch(
    "/books/{id}",
    response={201: None, 400: schema.Error},
    tags=["admin"],
    auth=django_auth_superuser,
)
def update_book(request, id: int, book: schema.BookPatchSchema):
    """Update a book"""
    try:
        book = Book.objects.get(id=id)
        book.title = book.title
        book.author = Author.objects.get(id=book.author_id)
        book.language = Language.objects.get(id=book.language_id)
        book.summary = book.summary
        book.isbn = book.isbn
        book.genre = book.genre
        book.save()
        return
    except ObjectDoesNotExist:
        return 400, {"message": "Book PATCH_FAILED"}


@api.patch(
    "/books/{id}/genre",
    response={201: None, 400: schema.Error},
    tags=["admin"],
    auth=django_auth_superuser,
)
def update_book_genre(request, id: int, genre_id: int):
    """Update a book genre"""
    try:
        book = Book.objects.get(id=id)
        book.genre = Genre.objects.get(id=genre_id)
        book.save()
        return
    except ObjectDoesNotExist:
        return 400, {"message": "Book Genre PATCH_FAILED"}


@api.delete(
    "/books/{id}",
    response={204: None, 404: schema.Error},
    tags=["admin"],
    auth=django_auth_superuser,
)
def delete_book(request, id: int):
    """Delete a book"""
    try:
        book = Book.objects.get(id=id)
        book.delete()
        return
    except ObjectDoesNotExist:
        return 404, {"message": "Book NOT_FOUND"}


@api.post("/authors", response={201: None}, tags=["admin"], auth=django_auth_superuser)
def create_author(request, author: schema.AuthorCreateSchema):
    """Create a new author"""
    Author.objects.create(
        first_name=author.first_name,
        last_name=author.last_name,
        date_of_birth=author.date_of_birth,
        date_of_death=author.date_of_death,
    )
    return


@api.patch(
    "/authors/{id}",
    response={201: None, 400: schema.Error},
    tags=["admin"],
    auth=django_auth_superuser,
)
def update_author(request, id: int, author: schema.AuthorPatchSchema):
    """Update an author"""
    try:
        author = Author.objects.get(id=id)
        author.first_name = author.first_name
        author.last_name = author.last_name
        author.date_of_birth = author.date_of_birth
        author.date_of_death = author.date_of_death
        author.save()
        return
    except ObjectDoesNotExist:
        return 400, {"message": "Author PATCH_FAILED"}


@api.delete(
    "/authors/{id}",
    response={204: None, 404: schema.Error},
    tags=["admin"],
    auth=django_auth_superuser,
)
def delete_author(request, id: int):
    """Delete an author"""
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return
    except ObjectDoesNotExist:
        return 404, {"message": "Author NOT_FOUND"}


@api.post(
    "/genres",
    response={201: None, 400: schema.Error},
    tags=["admin"],
    auth=django_auth_superuser,
)
def create_genre(request, genre: schema.GenreCreateSchema):
    """Create a new genre"""
    try:
        Genre.objects.create(name=genre.name)
        return
    except Exception:
        return 400, {"message": "Genre CREATE_FAILED"}


@api.patch(
    "/genres/{id}",
    response={201: None, 400: schema.Error},
    tags=["admin"],
    auth=django_auth_superuser,
)
def update_genre(request, id: int, genre: schema.GenreCreateSchema):
    """Update a genre"""
    try:
        genre = Genre.objects.get(id=id)
        genre.name = genre.name
        genre.save()
        return
    except ObjectDoesNotExist:
        return 400, {"message": "Genre PATCH_FAILED"}


@api.delete(
    "/genres/{id}",
    response={204: None, 404: schema.Error},
    tags=["admin"],
    auth=django_auth_superuser,
)
def delete_genre(request, id: int):
    """Delete a genre"""
    try:
        genre = Genre.objects.get(id=id)
        genre.delete()
        return
    except ObjectDoesNotExist:
        return 404, {"message": "Genre NOT_FOUND"}
