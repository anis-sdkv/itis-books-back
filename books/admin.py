# from django.contrib import admin
# from .models import Book, Person, Language, Subject, Bookshelf, Format, Summary
#
#
# @admin.register(Person)
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ['name', 'birth_year', 'death_year']
#     search_fields = ['name']
#     list_filter = ['birth_year', 'death_year']
#     ordering = ['name']
#
#
# class FormatInline(admin.TabularInline):
#     model = Format
#     extra = 0
#
#
# class SummaryInline(admin.TabularInline):
#     model = Summary
#     extra = 0
#
#
# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ['title', 'gutenberg_id', 'download_count', 'media_type']
#     search_fields = ['title', 'authors__name']
#     list_filter = ['media_type', 'copyright', 'languages__code']
#     filter_horizontal = ['authors', 'translators', 'languages', 'subjects', 'bookshelves']
#     ordering = ['-download_count']
#     inlines = [FormatInline, SummaryInline]
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).prefetch_related('authors')
#
#
# @admin.register(Language)
# class LanguageAdmin(admin.ModelAdmin):
#     list_display = ['code']
#     search_fields = ['code']
#
#
# @admin.register(Subject)
# class SubjectAdmin(admin.ModelAdmin):
#     list_display = ['name']
#     search_fields = ['name']
#
#
# @admin.register(Bookshelf)
# class BookshelfAdmin(admin.ModelAdmin):
#     list_display = ['name']
#     search_fields = ['name']
#
#
# @admin.register(Format)
# class FormatAdmin(admin.ModelAdmin):
#     list_display = ['book', 'mime_type', 'url']
#     list_filter = ['mime_type']
#     search_fields = ['book__title']
#
#
# @admin.register(Summary)
# class SummaryAdmin(admin.ModelAdmin):
#     list_display = ['book', 'text_preview']
#     search_fields = ['book__title', 'text']
#
#     def text_preview(self, obj):
#         return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
#
#     text_preview.short_description = 'Превью текста'