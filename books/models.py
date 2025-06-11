from django.db import models

class Person(models.Model):
    """Модель для авторов и переводчиков"""
    birth_year = models.SmallIntegerField(null=True, blank=True)
    death_year = models.SmallIntegerField(null=True, blank=True)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'books_person'
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'

    def __str__(self):
        return self.name

class Language(models.Model):
    """Модель для языков"""
    code = models.CharField(max_length=4, unique=True)

    class Meta:
        db_table = 'books_language'
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

    def __str__(self):
        return self.code


class Subject(models.Model):
    """Модель для тематик/предметов"""
    name = models.CharField(max_length=256)

    class Meta:
        db_table = 'books_subject'
        verbose_name = 'Тематика'
        verbose_name_plural = 'Тематики'

    def __str__(self):
        return self.name


class Bookshelf(models.Model):
    """Модель для книжных полок/категорий"""
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'books_bookshelf'
        verbose_name = 'Книжная полка'
        verbose_name_plural = 'Книжные полки'

    def __str__(self):
        return self.name


class Book(models.Model):
    """Модель для книг"""
    gutenberg_id = models.IntegerField(primary_key=True, unique=True)
    download_count = models.IntegerField(null=True, blank=True)
    media_type = models.CharField(max_length=16)
    title = models.CharField(max_length=1024, null=True, blank=True)
    copyright = models.BooleanField(null=True, blank=True)

    # Many-to-many relationships
    authors = models.ManyToManyField(
        Person,
        through='BookAuthor',
        related_name='authored_books'
    )
    translators = models.ManyToManyField(
        Person,
        through='BookTranslator',
        related_name='translated_books'
    )
    languages = models.ManyToManyField(Language, through='BookLanguage')
    subjects = models.ManyToManyField(Subject, through='BookSubject')
    bookshelves = models.ManyToManyField(Bookshelf, through='BookBookshelf')

    class Meta:
        db_table = 'books_book'
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title or f'Book {self.gutenberg_id}'


class BookAuthor(models.Model):
    """Промежуточная модель для связи книг и авторов"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_authors'
        unique_together = ('book', 'person')


class BookTranslator(models.Model):
    """Промежуточная модель для связи книг и переводчиков"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_translators'
        unique_together = ('book', 'person')


class BookLanguage(models.Model):
    """Промежуточная модель для связи книг и языков"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_languages'
        unique_together = ('book', 'language')


class BookSubject(models.Model):
    """Промежуточная модель для связи книг и тематик"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_subjects'
        unique_together = ('book', 'subject')


class BookBookshelf(models.Model):
    """Промежуточная модель для связи книг и полок"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookshelf = models.ForeignKey(Bookshelf, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_bookshelves'
        unique_together = ('book', 'bookshelf')


class Format(models.Model):
    """Модель для форматов книг"""
    mime_type = models.CharField(max_length=32)
    url = models.CharField(max_length=256)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='formats')

    class Meta:
        db_table = 'books_format'
        verbose_name = 'Формат'
        verbose_name_plural = 'Форматы'

    def __str__(self):
        return f'{self.mime_type} - {self.book.title}'


class Summary(models.Model):
    """Модель для описаний книг"""
    text = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='summaries')

    class Meta:
        db_table = 'books_summary'
        verbose_name = 'Описание'
        verbose_name_plural = 'Описания'

    def __str__(self):
        return f'Summary for {self.book.title}'