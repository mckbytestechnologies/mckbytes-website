from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import now
from .models import Post, Tag, Category


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display  = ("name", "slug", "post_count")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "Posts"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # ── List view ────────────────────────────────────────────────────
    list_display   = (
        "thumbnail_preview", "title", "tag_list",
        "category", "is_published", "published_at", "read_time_display"
    )
    list_display_links = ("thumbnail_preview", "title")
    list_filter    = ("is_published", "category", "tags", "published_at")
    search_fields  = ("title", "body", "excerpt")
    list_editable  = ("is_published",)
    date_hierarchy = "published_at"
    ordering       = ("-published_at",)

    # ── Detail / edit form ───────────────────────────────────────────
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal   = ("tags",)          # nice two-panel widget for tags
    readonly_fields     = ("image_preview", "slug_note", "created_at", "updated_at")

    fieldsets = (
        ("📝 Content", {
            "fields": (
                "title", "slug", "slug_note",
                "featured_image", "image_preview",
                "body",
                "excerpt",
            )
        }),
        ("🏷️ Organisation", {
            "fields": ("category", "tags"),
        }),
        ("🚀 Publishing", {
            "fields": ("is_published", "published_at", "created_at", "updated_at"),
        }),
    )

    # ── Custom display helpers ───────────────────────────────────────
    def thumbnail_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="height:48px;width:72px;object-fit:cover;border-radius:4px;">',
                obj.featured_image.url
            )
        return format_html(
            '<div style="height:48px;width:72px;background:#e5e7eb;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:18px;">🖼️</div>'
        )
    thumbnail_preview.short_description = "Image"

    def tag_list(self, obj):
        tags = obj.tags.all()
        if not tags:
            return "—"
        badges = " ".join(
            f'<span style="background:#dbeafe;color:#1e40af;padding:2px 8px;border-radius:12px;font-size:11px;margin:1px;display:inline-block;">{t.name}</span>'
            for t in tags
        )
        return format_html(badges)
    tag_list.short_description = "Tags"

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width:400px;max-height:220px;object-fit:cover;border-radius:8px;margin-top:6px;">',
                obj.featured_image.url
            )
        return "No image uploaded yet."
    image_preview.short_description = "Current Image Preview"

    def slug_note(self, obj):
        if obj.slug:
            return format_html(
                '<span style="color:#6b7280;font-size:12px;">URL will be: <code>/blog/{}/</code></span>',
                obj.slug
            )
        return format_html('<span style="color:#9ca3af;font-size:12px;">Auto-generated from title on save</span>')
    slug_note.short_description = ""

    def read_time_display(self, obj):
        return f"{obj.read_time()} min read"
    read_time_display.short_description = "Read Time"

    # ── Bulk action: publish selected ────────────────────────────────
    actions = ["publish_posts", "unpublish_posts"]

    def publish_posts(self, request, queryset):
        updated = queryset.update(is_published=True, published_at=now())
        self.message_user(request, f"{updated} post(s) published.")
    publish_posts.short_description = "✅ Publish selected posts"

    def unpublish_posts(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} post(s) unpublished.")
    unpublish_posts.short_description = "🚫 Unpublish selected posts"
