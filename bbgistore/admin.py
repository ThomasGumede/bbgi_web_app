from django.contrib import admin
from bbgistore.models.abstract import StoreCategory, Person
from bbgistore.models.book import Book, BookFile, BookDownload
from bbgistore.models.webinar import Webinar, WebinarVideo

@admin.register(StoreCategory)
class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_names", )
    search_fields = ("full_names", )

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "book_format", "number_of_pages", "added_by")
    list_filter = ("book_format", "added_by")
    search_fields = ("title", "authors__full_names")
    prepopulated_fields = {"slug": ("title",)}
    
@admin.register(BookFile)
class BookFileAdmin(admin.ModelAdmin):
    list_display = ("book", "extension", "version", "file_size")
    list_filter = ("extension",)
    search_fields = ("book__title",)

# Register your models here.
