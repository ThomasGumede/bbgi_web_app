import magic
from django.core.exceptions import ValidationError
from django.utils.text import slugify

def generate_unique_slug(instance, value, slug_field="slug"):
    slug = slugify(value)
    unique_slug = slug
    num = 1

    Model = instance.__class__

    while Model.objects.filter(**{slug_field: unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f"{slug}-{num}"
        num += 1

    return unique_slug

def validate_recap_video_file_size(file):
    """
    Validate the file size of the recap video.
    """
    max_file_size = 5 * 1024 * 1024  # 5 MB in bytes
    if file.size > max_file_size:
        raise ValidationError(f"Recap video file size should not exceed 5 MB. Current size: {file.size / (1024 * 1024):.2f} MB")
    

def validate_file_type(file):
    """
    Validate the file type based on its MIME type.
    """
    # Define allowed MIME types
    allowed_mime_types = [
        'application/pdf',  # PDF
        'application/epub+zip',  # EPUB
        'application/x-mobipocket-ebook',  # MOBI
        'application/vnd.amazon.ebook',  # AZW3
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # DOCX
    ]

    # Read the first few bytes of the file to determine its MIME type
    file.seek(0)  # Ensure we're at the start of the file
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)  # Reset the file pointer to the beginning

    if mime_type not in allowed_mime_types:
        raise ValidationError(f"Unsupported file type: {mime_type}. Allowed types are: {', '.join(allowed_mime_types)}")
    
def validate_video_file_type(file):
    """
    Validate the video file type based on its MIME type.
    """
    # Define allowed MIME types for video files
    allowed_mime_types = [
        'video/mp4',  # MP4
        'video/x-msvideo',  # AVI
        'video/x-matroska',  # MKV
        'video/quicktime',  # MOV
        'video/webm',  # WebM
    ]

    # Read the first few bytes of the file to determine its MIME type
    file.seek(0)  # Ensure we're at the start of the file
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)  # Reset the file pointer to the beginning

    if mime_type not in allowed_mime_types:
        raise ValidationError(f"Unsupported video file type: {mime_type}. Allowed types are: {', '.join(allowed_mime_types)}")