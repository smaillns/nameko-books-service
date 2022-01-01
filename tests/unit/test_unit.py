from books.models import Book, Author, GenderEnum


def test_can_create_author(db_session):
    author = Author(
        name='name',
        gender='Male'
    )
    db_session.add(author)
    db_session.commit()
    assert author.id > 0
    assert author.gender == GenderEnum.Male


def test_can_create_book(db_session):
    author = Author(name='author name', gender=GenderEnum.Male)
    db_session.add(author)
    db_session.commit()

    book = Book(
        author=author,
        title='Book Title'
    )
    db_session.add(book)
    db_session.commit()

    assert book.id > 0
    assert book.title == 'Book Title'
    assert book.author_id == author.id
