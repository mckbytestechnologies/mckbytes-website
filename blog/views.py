from django.shortcuts import render, get_object_or_404
from .models import Post, Tag, Category


def post_list(request):
    posts = Post.objects.filter(is_published=True).prefetch_related("tags")

    # Filter by tag
    tag_slug = request.GET.get("tag")
    active_tag = None
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)

    # Filter by category
    category_slug = request.GET.get("category")
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=active_category)

    context = {
        "posts":           posts,
        "tags":            Tag.objects.all(),
        "categories":      Category.objects.all(),
        "active_tag":      active_tag,
        "active_category": active_category,
    }
    return render(request, "blog/post_list.html", context)


def post_detail(request, slug):
    post    = get_object_or_404(Post, slug=slug, is_published=True)
    related = Post.objects.filter(
        is_published=True
    ).filter(
        tags__in=post.tags.all()
    ).exclude(pk=post.pk).distinct()[:3]

    context = {
        "post":    post,
        "related": related,
    }
    return render(request, "blog/post_detail.html", context)
