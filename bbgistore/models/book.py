from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import AbstractCreate
from django.contrib.auth import get_user_model
from bbgistore.models.abstract import StoreCategory, StoreItem, Person
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify
from bbgistore.utilities.validators import generate_unique_slug, validate_file_type
from pypdf import PdfReader
from pathlib import Path
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat

class Book(StoreItem):
    book_review_file = models.FileField(upload_to="bbgistore/book_reviews/", help_text=_("Provide a PDF file containing the book review"), null=True, blank=True, validators=[validate_file_type]) 
    category = models.ForeignKey(StoreCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="books", help_text=_("Select category for this book"))
    isbn = models.CharField(max_length=20, blank=True,unique=True, help_text=_("Provide ISBN for this book"))
    edition = models.CharField(max_length=200, blank=True, help_text=_("Provide edition e.g 1st Edition"))
    publisher = models.CharField(max_length=200, blank=True, help_text=_("Provide publisher e.g Juta"))
    publication_date = models.DateField(null=True, blank=True)
    number_of_pages = models.PositiveIntegerField(validators=[MinValueValidator(1, _("Number of pages in book should be more that 1"))], blank=True, null=True)
    book_format = models.CharField(max_length=100, default="ebook", help_text=_("Currently, only eletronic books are sold"), editable=False)
    authors = models.ManyToManyField(Person, related_name="books", blank=True, null=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="books", help_text=_("The person who added this book."))

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["-created"]
        
    @property
    def get_first_author(self):
        first_author = self.authors.first()
        return first_author.full_names if first_author else "Unknown Author"
    
    @property
    def get_all_authors(self):
        authors = self.authors.all()
        return ", ".join(f"{author.full_names}(Author)" for author in authors) if authors else "Unknown Author"
    
    @property
    def get_other_book_format(self):
        files = self.bookfiles.all()
        return ", ".join(f"{file.extension.upper()}(File)" for file in files) if files else "No other formats available"

    def save(self, *args, **kwargs):
        # Ensure the book_format is always set to "ebook"
        self.book_format = "ebook"
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title)
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
        upload_to="books/", null=True, blank=True, help_text=_("Upload book file")
    )
    book_file_link = models.URLField(null=True, blank=True, help_text=_("Provide a book file link e.g google drive, cloud drive, etc"))
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
        return f"{self.book.title} ({self.extension.upper()})"
    
    @property
    def file_size_in_mb(self):
        return round(self.file_size / (1024 * 1024), 2)  # Convert bytes to MB and round to 2 decimal places
    
    @property
    def formatted_size(self):
        return filesizeformat(self.file_size)
    
    @property
    def total_downloads(self):
        return self.downloads.aggregate(total=models.Sum('download_count'))['total'] or 0
    
    class Meta:
        verbose_name = "Book File"
        verbose_name_plural = "Book Files"
        ordering = ["-created"]
        constraints = [
        models.UniqueConstraint(
            fields=["book", "extension"],
            name="unique_book_extension"
        )
    ]
        
    def clean(self):
        from urllib.parse import urlparse
        super().clean()
        if not self.file and not self.book_file_link:
            raise ValidationError("Please provide atleast one book source, either book link or book file")
        
        if self.file and self.book_file_link:
            raise ValidationError(
                "Provide either a file or a download link, not both."
            )
        
        if self.book_file_link:
            parse = urlparse(self.book_file_link)
            if not parse.scheme:
                self.book_file_link = f"https://{self.book_file_link}"
        
    def save(self, *args, **kwargs):
        # Update file_size and checksum when saving
        
        if self.file and not self.pk:
            reader = PdfReader(self.file)

           
            self.file_size = self.file.size
            self.extension = Path(self.file.name).suffix.replace(".", "").lower()
            if Path(self.file.name).suffix.replace(".", "").lower() == "pdf":
                reader = PdfReader(self.file)
                pages = len(reader.pages)

                if self.book.number_of_pages != pages:
                    self.book.number_of_pages = pages
                    self.book.save(update_fields=["number_of_pages"])
                
                
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

