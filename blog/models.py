from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    # ── Core fields ──────────────────────────────
    title          = models.CharField(max_length=200)
    slug           = models.SlugField(unique=True, blank=True, max_length=220)
    featured_image = models.ImageField(
        upload_to="upload-blog/",
        blank=True, null=True,
        help_text="Recommended: 1200×630 px"
    )
    body           = models.TextField(
        help_text="Write your full post content here. Basic HTML tags are supported."
    )
    tags           = models.ManyToManyField(Tag, blank=True, related_name="posts")

    # ── Supporting fields ────────────────────────────
    category       = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='posts'  # ← ADD THIS - allows Category.posts.all()
    )
    excerpt        = models.TextField(
        max_length=300, blank=True,
        help_text="Short summary shown on listing page (auto-filled from body if left blank)"
    )
    is_published   = models.BooleanField(default=False)
    published_at   = models.DateTimeField(blank=True, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    views          = models.IntegerField(default=0)  # ← Also add this field

    # ── Auto-generate slug from title; auto-fill excerpt ────────────
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        if not self.excerpt and self.body:
            import re
            plain = re.sub(r"<[^>]+>", "", self.body)
            self.excerpt = plain[:280].rsplit(" ", 1)[0] + "…" if len(plain) > 280 else plain
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    def read_time(self):
        """Estimated reading time in minutes."""
        import re
        word_count = len(re.sub(r"<[^>]+>", "", self.body).split())
        return max(1, round(word_count / 200))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published_at", "-created_at"]
        