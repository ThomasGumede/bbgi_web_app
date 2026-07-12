from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import AbstractCreate
from django.contrib.auth import get_user_model
from bbgistore.models.abstract import StoreCategory, StoreItem, Person
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify
from pypdf import PdfReader

class Book(StoreItem):
    category = models.ForeignKey(StoreCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="books", help_text=_("Select category for this book"))
    isbn = models.CharField(max_length=20, blank=True,unique=True, help_text=_("Provide ISBN for this book"))
    edition = models.CharField(max_length=200, blank=True, help_text=_("Provide edition e.g 1st Edition"))
    publisher = models.CharField(max_length=200, blank=True, help_text=_("Provide publisher e.g Juta"))
    publication_date = models.DateField(null=True, blank=True)
    number_of_pages = models.PositiveIntegerField(validators=[MinValueValidator(1, _("Number of pages in book should be more that 1"))])
    book_format = models.CharField(max_length=100, default="ebook", help_text=_("Currently, only eletronic books are sold"), editable=False)
    authors = models.ManyToManyField(Person, related_name="books", blank=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["-created"]
        
    def save(self, *args, **kwargs):
        # Ensure the book_format is always set to "ebook"
        self.book_format = "ebook"
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BookFile(AbstractCreate):
    class Extension(models.TextChoices):
        PDF = "pdf", _("PDF")
        EPUB = "epub", _("EPUB")
        MOBI = "mobi", _("MOBI")
        AZW3 = "azw3", _("AZW3")
        DOCX = "docx", _("DOCX")
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="bookfiles")
    extension = models.CharField(
        max_length=10,
        choices=Extension.choices, default=Extension.PDF,
    )

    file = models.FileField(
        upload_to="books/",
    )

    version = models.CharField(
        max_length=50,
        default="1.0",
    )

    file_size = models.PositiveBigIntegerField(
        default=0,
        help_text="File size in bytes.",
    )

    checksum = models.CharField(
        max_length=64,
        blank=True,
        help_text="Optional SHA-256 checksum.",
    )

    is_active = models.BooleanField(
        default=True,
    )
    download_limit = models.PositiveIntegerField(validators=[MinValueValidator(1, _("Number of downloads should be more than 1"))], default=5)
    
    def __str__(self):
        return f"{self.book.title} file"
    
    @property
    def file_size_in_mb(self):
        return round(self.file_size / (1024 * 1024), 2)  # Convert bytes to MB and round to 2 decimal places
    
    @property
    def total_downloads(self):
        return self.downloads.aggregate(total=models.Sum('download_count'))['total'] or 0
    
    class Meta:
        verbose_name = "Book File"
        verbose_name_plural = "Book Files"
        ordering = ["-created"]
        
    def save(self, *args, **kwargs):
        # Update file_size and checksum when saving
        
        if self.file:
            reader = PdfReader(self.file)
            self.book.number_of_pages = len(reader.pages)
            self.book.save(update_fields=['number_of_pages'])
           
            self.file_size = self.file.size
            self.extension = self.file.name.split('.')[-1].lower()
            import hashlib
            sha256 = hashlib.sha256()
            for chunk in self.file.chunks():
                sha256.update(chunk)
            self.checksum = sha256.hexdigest()
            
            self.file.seek(0)  # Reset the file pointer to the beginning after reading for checksum
        super().save(*args, **kwargs)
        
class BookDownload(AbstractCreate):
    book_file = models.ForeignKey(BookFile, on_delete=models.CASCADE, related_name="downloads")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="book_downloads")
    download_count = models.PositiveIntegerField(default=0)
    last_downloaded = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Book Download"
        verbose_name_plural = "Book Downloads"
        unique_together = ("book_file", "user")

