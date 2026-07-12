from django.contrib import admin
from django.db.models import Count
from bbgistore.models.abstract import StoreCategory, Person
from bbgistore.models.book import Book, BookFile, BookDownload
from bbgistore.models.webinar import Webinar, WebinarVideo
from django.utils.html import format_html


# ==========================================================
# INLINES
# ==========================================================

class BookFileInline(admin.StackedInline):
    model = BookFile
    extra = 0
    fields = (
        "extension",
        "file",
        "book_file_link",
        "version",
        "download_limit",
        "is_active",
    )


class WebinarVideoInline(admin.StackedInline):
    model = WebinarVideo
    extra = 0
    fields = (
        "video",
        "video_link",
        "is_bonus",
    )


# ==========================================================
# CATEGORY
# ==========================================================

@admin.register(StoreCategory)
class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "book_count",
    )


    search_fields = (
        "title",
        
    )


    ordering = (
        "title",
    )

    exclude = (
        "slug",
    )

    @admin.display(description="Books")
    def book_count(self, obj):
        return obj.books.count()

    


# ==========================================================
# AUTHORS
# ==========================================================

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "photo",
        "full_names",
        "bbgi_account",
        "book_count",
        "webinar_count",
        "created",
    )

    list_display_links = (
        "photo",
        "full_names",
    )

    search_fields = (
        "full_names",
        "bbgi_account__first_name",
        "bbgi_account__last_name",
        "bbgi_account__email",
        "bbgi_account__username",
    )

    autocomplete_fields = (
        "bbgi_account",
    )

    readonly_fields = (
        "created",
        "updated",
        "photo_preview",
        "book_count",
        "webinar_count",
    )

    ordering = (
        "full_names",
    )

    list_per_page = 25

    fieldsets = (
        (
            "Personal Information",
            {
                "fields": (
                    "full_names",
                    "bbgi_account",
                )
            },
        ),
        (
            "Profile",
            {
                "fields": (
                    "thumbnail",
                    "photo_preview",
                    "biography",
                )
            },
        ),
        (
            "Statistics",
            {
                "classes": ("collapse",),
                "fields": (
                    "book_count",
                    "webinar_count",
                ),
            },
        ),
        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created",
                    "updated",
                ),
            },
        ),
    )

    actions = (
        "clear_profile_photos",
    )

    @admin.display(description="Photo")
    def photo(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width:45px;height:45px;'
                'border-radius:50%;object-fit:cover;" />',
                obj.thumbnail.url,
            )
        return "—"

    @admin.display(description="Profile Preview")
    def photo_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-height:180px;'
                'border-radius:10px;" />',
                obj.thumbnail.url,
            )
        return "No profile image uploaded."

    @admin.display(description="Books")
    def book_count(self, obj):
        return obj.books.count()

    @admin.display(description="Webinars")
    def webinar_count(self, obj):
        return obj.webinars.count()

    @admin.action(description="Remove selected profile photos")
    def clear_profile_photos(self, request, queryset):
        queryset.update(thumbnail="")
        self.message_user(
            request,
            f"{queryset.count()} profile photo(s) removed."
        )


# ==========================================================
# BOOK
# ==========================================================
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "cover",
        "title",
        "category",
        "first_author",
        "price",
        "status_badge",
        "featured",
        "is_active",
        "file_formats",
        "downloads",
        "created",
    )

    list_display_links = (
        "cover",
        "title",
    )

    list_editable = (
        "featured",
        "is_active",
    )

    list_filter = (
        "status",
        "featured",
        "is_active",
        "category",
        "publication_date",
        "created",
    )

    search_fields = (
        "title",
        "isbn",
        "publisher",
        "authors__full_names",
        "category__title",
    )

    autocomplete_fields = (
        "authors",
        "category",
        "added_by",
    )

    readonly_fields = (
        "slug",
        "book_format",
        "cover_preview",
        "downloads",
        "created",
        "updated",
    )

    exclude = (
        "slug",
    )

    filter_horizontal = (
        "authors",
        
    )

    ordering = (
        "-created",
    )

    list_per_page = 25

    save_on_top = True

    inlines = (
        BookFileInline,
    )

    fieldsets = (
        (
            "Book Information",
            {
                "fields": (
                    "title",
                    "short_description",
                    "description",
                    "thumbnail",
                    "cover_preview",
                    "recap_video",
                )
            },
        ),
        (
            "Publication",
            {
                "fields": (
                    "authors",
                    "category",
                    "publisher",
                    "edition",
                    "isbn",
                    "publication_date",
                    "number_of_pages",
                    "book_review_file",
                )
            },
        ),
        (
            "Store",
            {
                "fields": (
                    "price",
                    "status",
                    "featured",
                    "is_active",
                    "tags",
                )
            },
        ),
        (
            "System",
            {
                "classes": ("collapse",),
                "fields": (
                    "book_format",
                    "added_by",
                    "downloads",
                    "created",
                    "updated",
                ),
            },
        ),
    )

    actions = (
        "publish_books",
        "draft_books",
        "feature_books",
        "remove_featured",
        "activate_books",
        "deactivate_books",
        "mark_free",
    )

    @admin.display(description="Cover")
    def cover(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="height:60px;width:45px;object-fit:cover;border-radius:6px;" />',
                obj.thumbnail.url,
            )
        return "-"

    @admin.display(description="Preview")
    def cover_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-height:220px;border-radius:8px;" />',
                obj.thumbnail.url,
            )
        return "No cover uploaded."

    @admin.display(description="Author")
    def first_author(self, obj):
        return obj.get_first_author

    @admin.display(description="Formats")
    def file_formats(self, obj):
        return obj.get_other_book_format

    @admin.display(description="Downloads")
    def downloads(self, obj):
        return sum(
            file.total_downloads
            for file in obj.bookfiles.all()
        )

    @admin.display(description="Status")
    def status_badge(self, obj):
        colour = "#16a34a" if obj.status == "published" else "#d97706"

        return format_html(
            '<strong style="color:{};">{}</strong>',
            colour,
            obj.get_status_display(),
        )

    @admin.action(description="Publish selected books")
    def publish_books(self, request, queryset):
        updated = queryset.update(status="published")
        self.message_user(request, f"{updated} book(s) published.")

    @admin.action(description="Move selected books to draft")
    def draft_books(self, request, queryset):
        updated = queryset.update(status="draft")
        self.message_user(request, f"{updated} book(s) moved to draft.")

    @admin.action(description="Feature selected books")
    def feature_books(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f"{updated} featured book(s).")

    @admin.action(description="Remove featured status")
    def remove_featured(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f"{updated} book(s) updated.")

    @admin.action(description="Activate selected books")
    def activate_books(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} book(s) activated.")

    @admin.action(description="Deactivate selected books")
    def deactivate_books(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} book(s) deactivated.")

    @admin.action(description="Mark selected books as free")
    def mark_free(self, request, queryset):
        updated = queryset.update(price=0)
        self.message_user(request, f"{updated} book(s) marked as free.")

# ==========================================================
# BOOK FILES
# ==========================================================
@admin.register(BookFile)
class BookFileAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "extension_badge",
        "version",
        "file_size_display",
        "download_limit",
        "downloads",
        "is_active",
        "created",
    )

    list_display_links = (
        "book",
    )

    list_editable = (
        "download_limit",
        "is_active",
    )

    list_filter = (
        "extension",
        "is_active",
        "created",
    )

    search_fields = (
        "book__title",
        "checksum",
        "version",
    )

    autocomplete_fields = (
        "book",
    )

    readonly_fields = (
        "file_size",
        "file_size_display",
        "checksum",
        "downloads",
        "created",
        "updated",
    )

    ordering = (
        "-created",
    )

    list_per_page = 25

    save_on_top = True

    fieldsets = (
        (
            "Book File",
            {
                "fields": (
                    "book",
                    "extension",
                    "file",
                    "book_file_link",
                    "version",
                )
            },
        ),
        (
            "Downloads",
            {
                "fields": (
                    "download_limit",
                    "downloads",
                    "is_active",
                )
            },
        ),
        (
            "File Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "file_size",
                    "file_size_display",
                    "checksum",
                )
            },
        ),
        (
            "System",
            {
                "classes": ("collapse",),
                "fields": (
                    "created",
                    "updated",
                )
            },
        ),
    )

    actions = (
        "activate_files",
        "deactivate_files",
        "reset_download_limits",
    )

    @admin.display(description="Extension")
    def extension_badge(self, obj):
        colours = {
            "pdf": "#dc2626",
            "epub": "#16a34a",
            "mobi": "#2563eb",
            "azw3": "#9333ea",
            "docx": "#0284c7",
        }

        colour = colours.get(obj.extension, "#6b7280")

        return format_html(
            '<span style="'
            'background:{};'
            'color:white;'
            'padding:4px 8px;'
            'border-radius:6px;'
            'font-size:11px;'
            'font-weight:bold;">{}</span>',
            colour,
            obj.extension.upper(),
        )

    @admin.display(description="File Size")
    def file_size_display(self, obj):
        return f"{obj.file_size_in_mb} MB"

    @admin.display(description="Downloads")
    def downloads(self, obj):
        return obj.total_downloads

    @admin.action(description="Activate selected files")
    def activate_files(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} file(s) activated.")

    @admin.action(description="Deactivate selected files")
    def deactivate_files(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} file(s) deactivated.")

    @admin.action(description="Reset download limit to 5")
    def reset_download_limits(self, request, queryset):
        updated = queryset.update(download_limit=5)
        self.message_user(
            request,
            f"{updated} file(s) reset to a download limit of 5."
        )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("book")
            .prefetch_related("downloads")
        )

# ==========================================================
# DOWNLOADS
# ==========================================================

@admin.register(BookDownload)
class BookDownloadAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "book",
        "book_file",
        "download_count",
        "last_downloaded",
        "created",
    )

    list_display_links = (
        "user",
        "book",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "book_file__book__title",
    )

    list_filter = (
        "book_file__extension",
        "last_downloaded",
        "created",
    )

    autocomplete_fields = (
        "user",
        "book_file",
    )

    readonly_fields = (
        "user",
        "book_file",
        "book",
        "download_count",
        "last_downloaded",
        "created",
        "updated",
    )

    ordering = (
        "-last_downloaded",
    )

    list_per_page = 50

    date_hierarchy = "last_downloaded"

    actions = (
        "reset_download_counts",
    )

    fieldsets = (
        (
            "Download Information",
            {
                "fields": (
                    "user",
                    "book",
                    "book_file",
                    "download_count",
                    "last_downloaded",
                )
            },
        ),
        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created",
                    "updated",
                )
            },
        ),
    )

    @admin.display(description="Book")
    def book(self, obj):
        return obj.book_file.book

    @admin.action(description="Reset download counts")
    def reset_download_counts(self, request, queryset):
        updated = queryset.update(download_count=0)
        self.message_user(
            request,
            f"{updated} download record(s) reset."
        )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "user",
                "book_file",
                "book_file__book",
            )
        )

    # Prevent manual creation
    def has_add_permission(self, request):
        return False

    # Prevent editing
    def has_change_permission(self, request, obj=None):
        return False

    # Allow viewing
    def has_view_permission(self, request, obj=None):
        return True

# ==========================================================
# WEBINARS
# ==========================================================

@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail_preview",
        "title",
        "category",
        "webinar_type",
        "level",
        "presenters_display",
        "price",
        "status_badge",
        "featured",
        "is_active",
        "video_count",
        "created",
    )

    list_display_links = (
        "thumbnail_preview",
        "title",
    )

    list_editable = (
        "featured",
        "is_active",
    )

    list_filter = (
        "status",
        "featured",
        "is_active",
        "webinar_type",
        "level",
        "certificate_available",
        "replay_available",
        "category",
        "created",
    )

    search_fields = (
        "title",
        "short_description",
        "description",
        "presenters__full_names",
        "category__title",
    )

    autocomplete_fields = (
        "category",
        "presenters",
        "added_by",
    )

    filter_horizontal = (
        "presenters",
        
    )

    readonly_fields = (
        "thumbnail_large",
        "video_count",
        "created",
        "updated",
    )

    exclude = (
        "slug",
    )

    ordering = (
        "-created",
    )

    save_on_top = True

    list_per_page = 25

    inlines = (
        WebinarVideoInline,
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "title",
                    "short_description",
                    "description",
                    "thumbnail",
                    "thumbnail_large",
                    "recap_video",
                )
            },
        ),
        (
            "Presenters & Category",
            {
                "fields": (
                    "category",
                    "presenters",
                    "level",
                )
            },
        ),
        (
            "Webinar Details",
            {
                "fields": (
                    "webinar_type",
                    "duration",
                    "start_time",
                    "end_time",
                    "registration_deadline",
                    "max_participants",
                )
            },
        ),
        (
            "Certificates & CPD",
            {
                "fields": (
                    "certificate_available",
                    "cpd_points",
                    "replay_available",
                )
            },
        ),
        (
            "Store",
            {
                "fields": (
                    "price",
                    "status",
                    "featured",
                    "is_active",
                    "tags",
                )
            },
        ),
        (
            "System",
            {
                "classes": ("collapse",),
                "fields": (
                    "added_by",
                    "video_count",
                    "created",
                    "updated",
                )
            },
        ),
    )

    actions = (
        "publish_webinars",
        "draft_webinars",
        "feature_webinars",
        "remove_featured",
        "activate_webinars",
        "deactivate_webinars",
        "enable_certificates",
        "disable_certificates",
        "enable_replay",
        "disable_replay",
    )

    @admin.display(description="Thumbnail")
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="height:60px;width:90px;object-fit:cover;border-radius:6px;">',
                obj.thumbnail.url,
            )
        return "-"

    @admin.display(description="Preview")
    def thumbnail_large(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-height:220px;border-radius:8px;">',
                obj.thumbnail.url,
            )
        return "No thumbnail uploaded."

    @admin.display(description="Presenters")
    def presenters_display(self, obj):
        return obj.presenters_list or "-"

    @admin.display(description="Videos")
    def video_count(self, obj):
        return obj.webinarvideos.count()

    @admin.display(description="Status")
    def status_badge(self, obj):
        colour = "#16a34a" if obj.status == "published" else "#d97706"
        return format_html(
            '<strong style="color:{};">{}</strong>',
            colour,
            obj.get_status_display(),
        )

    @admin.action(description="Publish selected webinars")
    def publish_webinars(self, request, queryset):
        updated = queryset.update(status="published")
        self.message_user(request, f"{updated} webinar(s) published.")

    @admin.action(description="Move selected webinars to draft")
    def draft_webinars(self, request, queryset):
        updated = queryset.update(status="draft")
        self.message_user(request, f"{updated} webinar(s) moved to draft.")

    @admin.action(description="Feature selected webinars")
    def feature_webinars(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f"{updated} webinar(s) featured.")

    @admin.action(description="Remove featured status")
    def remove_featured(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f"{updated} webinar(s) updated.")

    @admin.action(description="Activate selected webinars")
    def activate_webinars(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} webinar(s) activated.")

    @admin.action(description="Deactivate selected webinars")
    def deactivate_webinars(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} webinar(s) deactivated.")

    @admin.action(description="Enable certificates")
    def enable_certificates(self, request, queryset):
        updated = queryset.update(certificate_available=True)
        self.message_user(request, f"Certificates enabled for {updated} webinar(s).")

    @admin.action(description="Disable certificates")
    def disable_certificates(self, request, queryset):
        updated = queryset.update(certificate_available=False)
        self.message_user(request, f"Certificates disabled for {updated} webinar(s).")

    @admin.action(description="Enable replay")
    def enable_replay(self, request, queryset):
        updated = queryset.update(replay_available=True)
        self.message_user(request, f"Replay enabled for {updated} webinar(s).")

    @admin.action(description="Disable replay")
    def disable_replay(self, request, queryset):
        updated = queryset.update(replay_available=False)
        self.message_user(request, f"Replay disabled for {updated} webinar(s).")

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.added_by:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("category", "added_by")
            .prefetch_related("presenters", "webinarvideos")
        )

# ==========================================================
# WEBINAR VIDEOS
# ==========================================================

@admin.register(WebinarVideo)
class WebinarVideoAdmin(admin.ModelAdmin):
    list_display = (
        "webinar",
        "video_name",
        "video_preview",
        "is_bonus",
        "created",
    )

    list_display_links = (
        "webinar",
        "video_name",
    )

    list_editable = (
        "is_bonus",
    )

    list_filter = (
        "is_bonus",
        "created",
    )

    search_fields = (
        "webinar__title",
        "video",
    )

    autocomplete_fields = (
        "webinar",
    )

    readonly_fields = (
        "video_preview_large",
        "created",
        "updated",
    )

    ordering = (
        "-created",
    )

    list_per_page = 25

    save_on_top = True

    fieldsets = (
        (
            "Webinar Video",
            {
                "fields": (
                    "webinar",
                    "video",
                    "video_link",
                    "video_preview_large",
                    "is_bonus",
                )
            },
        ),
        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created",
                    "updated",
                )
            },
        ),
    )

    actions = (
        "mark_as_bonus",
        "remove_bonus",
    )

    @admin.display(description="Video")
    def video_name(self, obj):
        if obj.video:
            return obj.video.name.split("/")[-1]
        return "-"

    @admin.display(description="Preview")
    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video width="120" height="70" controls preload="metadata">'
                '<source src="{}">'
                "</video>",
                obj.video.url,
            )
        return "-"

    @admin.display(description="Video Preview")
    def video_preview_large(self, obj):
        if obj.video:
            return format_html(
                '<video width="500" controls preload="metadata">'
                '<source src="{}">'
                "</video>",
                obj.video.url,
            )
        return "No video uploaded."

    @admin.action(description="Mark selected videos as bonus")
    def mark_as_bonus(self, request, queryset):
        updated = queryset.update(is_bonus=True)
        self.message_user(
            request,
            f"{updated} video(s) marked as bonus."
        )

    @admin.action(description="Remove bonus status")
    def remove_bonus(self, request, queryset):
        updated = queryset.update(is_bonus=False)
        self.message_user(
            request,
            f"{updated} video(s) updated."
        )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("webinar")
        )