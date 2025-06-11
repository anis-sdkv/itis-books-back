from rest_framework import serializers
from .models import Book, Person, Language, Subject, Bookshelf, Format


class PersonSerializer(serializers.ModelSerializer):
    """Сериализатор для авторов и переводчиков"""
    years = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ['id', 'name', 'birth_year', 'death_year', 'years']

    def get_years(self, obj):
        """Возвращает годы жизни в формате 'birth_year - death_year'"""
        if obj.birth_year and obj.death_year:
            return f"{obj.birth_year} - {obj.death_year}"
        elif obj.birth_year:
            return f"{obj.birth_year} - ?"
        elif obj.death_year:
            return f"? - {obj.death_year}"
        return None


class LanguageSerializer(serializers.ModelSerializer):
    """Сериализатор для языков"""

    class Meta:
        model = Language
        fields = ['id', 'code']


class SubjectSerializer(serializers.ModelSerializer):
    """Сериализатор для тематик"""

    class Meta:
        model = Subject
        fields = ['id', 'name']


class BookshelfSerializer(serializers.ModelSerializer):
    """Сериализатор для книжных полок"""

    class Meta:
        model = Bookshelf
        fields = ['id', 'name']


class FormatSerializer(serializers.ModelSerializer):
    """Сериализатор для форматов книг"""

    class Meta:
        model = Format
        fields = ['id', 'mime_type', 'url']


class BookListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка книг (краткая информация)"""
    authors = PersonSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'gutenberg_id',
            'title',
            'authors',
            'languages',
            'download_count',
            'media_type'
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о книге"""
    authors = PersonSerializer(many=True, read_only=True)
    translators = PersonSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    bookshelves = BookshelfSerializer(many=True, read_only=True)
    formats = FormatSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'gutenberg_id',
            'title',
            'authors',
            'translators',
            'languages',
            'subjects',
            'bookshelves',
            'formats',
            'download_count',
            'media_type',
            'copyright'
        ]


class PersonDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации об авторе"""
    authored_books = BookListSerializer(many=True, read_only=True)
    translated_books = BookListSerializer(many=True, read_only=True)
    years = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = [
            'id',
            'name',
            'birth_year',
            'death_year',
            'years',
            'authored_books',
            'translated_books'
        ]

    def get_years(self, obj):
        """Возвращает годы жизни в формате 'birth_year - death_year'"""
        if obj.birth_year and obj.death_year:
            return f"{obj.birth_year} - {obj.death_year}"
        elif obj.birth_year:
            return f"{obj.birth_year} - ?"
        elif obj.death_year:
            return f"? - {obj.death_year}"
        return None