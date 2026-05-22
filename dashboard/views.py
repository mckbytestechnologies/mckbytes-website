from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from blog.models import Post, Category, Tag
from contact.models import Contact
import hashlib
import re

# Fixed admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("pass123@".encode()).hexdigest()

def admin_login(request):
    """Custom admin login page"""
    if request.session.get('admin_logged_in'):
        return redirect('dashboard:dashboard_home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if username == ADMIN_USERNAME and password_hash == ADMIN_PASSWORD_HASH:
            request.session['admin_logged_in'] = True
            request.session['admin_username'] = username
            messages.success(request, 'Welcome to Admin Dashboard!')
            return redirect('dashboard:dashboard_home')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'dashboard/login.html')

def admin_logout(request):
    """Custom admin logout"""
    request.session.flush()
    messages.success(request, 'You have been logged out successfully!')
    return redirect('dashboard:admin_login')

def admin_required(view_func):
    """Decorator to check if admin is logged in"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_logged_in'):
            return redirect('dashboard:admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def dashboard_home(request):
    """Main dashboard view with statistics"""
    
    # Existing counts
    total_contacts = Contact.objects.count()
    total_blogs = Post.objects.count()
    published_blogs = Post.objects.filter(is_published=True).count()
    draft_blogs = Post.objects.filter(is_published=False).count()
    total_categories = Category.objects.count()
    total_tags = Tag.objects.count()
    
    # New job stats
    total_jobs = Job.objects.count()
    active_jobs = Job.objects.filter(is_active=True).count()
    total_applications = JobApplication.objects.count()
    pending_applications = JobApplication.objects.filter(status='pending').count()
    shortlisted_count = JobApplication.objects.filter(status='shortlisted').count()
    hired_count = JobApplication.objects.filter(status='hired').count()
    rejected_count = JobApplication.objects.filter(status='rejected').count()
    
    # Recent data
    recent_contacts = Contact.objects.order_by('-created_at')[:5]
    recent_blogs = Post.objects.order_by('-created_at')[:5]
    recent_applications = JobApplication.objects.order_by('-created_at')[:5]
    recent_contacts_count = Contact.objects.filter(created_at__month=timezone.now().month).count()
    
    # Monthly contacts chart
    now = timezone.now()
    months_data = []
    for i in range(5, -1, -1):
        month_date = now - timedelta(days=30 * i)
        count = Contact.objects.filter(
            created_at__year=month_date.year,
            created_at__month=month_date.month
        ).count()
        months_data.append({
            'month': month_date.strftime('%b'),
            'count': count
        })
    
    context = {
        'total_contacts': total_contacts,
        'total_blogs': total_blogs,
        'published_blogs': published_blogs,
        'draft_blogs': draft_blogs,
        'total_categories': total_categories,
        'total_tags': total_tags,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'shortlisted_count': shortlisted_count,
        'hired_count': hired_count,
        'rejected_count': rejected_count,
        'recent_contacts': recent_contacts,
        'recent_blogs': recent_blogs,
        'recent_applications': recent_applications,
        'recent_contacts_count': recent_contacts_count,
        'months_data': months_data,
        'active_page': 'dashboard',
    }
    return render(request, 'dashboard/home.html', context)

    
# ==================== CONTACT MANAGEMENT ====================

@admin_required
def contact_list(request):
    """List all contact messages"""
    contacts = Contact.objects.all().order_by('-created_at')
    
    # Search
    search = request.GET.get('search')
    if search:
        contacts = contacts.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(mobile__icontains=search) |
            Q(message__icontains=search)
        )
    
    paginator = Paginator(contacts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'contacts': page_obj,
        'total_count': Contact.objects.count(),
        'active_page': 'contacts',
    }
    return render(request, 'dashboard/contact_list.html', context)

@admin_required
def contact_detail(request, pk):
    """View single contact message"""
    contact = get_object_or_404(Contact, pk=pk)
    
    context = {
        'contact': contact,
        'active_page': 'contacts',
    }
    return render(request, 'dashboard/contact_detail.html', context)

@admin_required
def contact_delete(request, pk):
    """Delete contact message"""
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact message deleted successfully!')
        return redirect('dashboard:contact_list')
    
    context = {'contact': contact}
    return render(request, 'dashboard/contact_confirm_delete.html', context)

# ==================== BLOG MANAGEMENT ====================

@admin_required
def blog_list(request):
    """List all blog posts"""
    posts = Post.objects.all().order_by('-created_at')
    
    # Filter by status
    status = request.GET.get('status')
    if status == 'published':
        posts = posts.filter(is_published=True)
    elif status == 'draft':
        posts = posts.filter(is_published=False)
    
    # Search
    search = request.GET.get('search')
    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(excerpt__icontains=search)
        )
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'total_posts': Post.objects.count(),
        'published_count': Post.objects.filter(is_published=True).count(),
        'draft_count': Post.objects.filter(is_published=False).count(),
        'active_page': 'blog',
    }
    return render(request, 'dashboard/blog_list.html', context)

@admin_required
def blog_create(request):
    """Create new blog post"""
    if request.method == 'POST':
        title = request.POST.get('title')
        if not title:
            messages.error(request, 'Title is required!')
            return redirect('dashboard:blog_create')
        
        # Auto-generate slug from title
        import re
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        
        # Ensure unique slug
        original_slug = slug
        counter = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        # Get or create category
        category_name = request.POST.get('category')
        category = None
        if category_name:
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': re.sub(r'[^a-z0-9]+', '-', category_name.lower()).strip('-')}
            )
        
        # Create post
        post = Post.objects.create(
            title=title,
            slug=slug,
            category=category,
            excerpt=request.POST.get('excerpt', ''),
            body=request.POST.get('body', ''),
            is_published=request.POST.get('is_published') == 'on',
            published_at=timezone.now() if request.POST.get('is_published') == 'on' else None
        )
        
        # Handle tags
        tags_string = request.POST.get('tags', '')
        if tags_string:
            tag_names = [t.strip() for t in tags_string.split(',') if t.strip()]
            for tag_name in tag_names:
                tag_slug = re.sub(r'[^a-z0-9]+', '-', tag_name.lower()).strip('-')
                tag, _ = Tag.objects.get_or_create(name=tag_name, slug=tag_slug)
                post.tags.add(tag)
        
        # Handle featured image
        if request.FILES.get('featured_image'):
            post.featured_image = request.FILES['featured_image']
            post.save()
        
        messages.success(request, 'Blog post created successfully!')
        return redirect('dashboard:blog_list')
    
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'categories': categories,
        'tags': tags,
        'active_page': 'blog',
        'is_edit': False,
    }
    return render(request, 'dashboard/blog_form.html', context)

@admin_required
def blog_edit(request, pk):
    """Edit existing blog post"""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        
        # Handle category
        category_name = request.POST.get('category')
        if category_name:
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': re.sub(r'[^a-z0-9]+', '-', category_name.lower()).strip('-')}
            )
            post.category = category
        else:
            post.category = None
        
        post.excerpt = request.POST.get('excerpt', '')
        post.body = request.POST.get('body', '')
        post.is_published = request.POST.get('is_published') == 'on'
        
        if request.POST.get('is_published') == 'on' and not post.published_at:
            post.published_at = timezone.now()
        
        # Handle tags
        post.tags.clear()
        tags_string = request.POST.get('tags', '')
        if tags_string:
            tag_names = [t.strip() for t in tags_string.split(',') if t.strip()]
            for tag_name in tag_names:
                tag_slug = re.sub(r'[^a-z0-9]+', '-', tag_name.lower()).strip('-')
                tag, _ = Tag.objects.get_or_create(name=tag_name, slug=tag_slug)
                post.tags.add(tag)
        
        # Handle featured image
        if request.FILES.get('featured_image'):
            post.featured_image = request.FILES['featured_image']
        
        post.save()
        messages.success(request, 'Blog post updated successfully!')
        return redirect('dashboard:blog_list')
    
    categories = Category.objects.all()
    tags = Tag.objects.all()
    current_tags = ', '.join([tag.name for tag in post.tags.all()])
    
    context = {
        'post': post,
        'categories': categories,
        'tags': tags,
        'current_tags': current_tags,
        'active_page': 'blog',
        'is_edit': True,
    }
    return render(request, 'dashboard/blog_form.html', context)

@admin_required
def blog_delete(request, pk):
    """Delete blog post"""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('dashboard:blog_list')
    
    context = {'post': post}
    return render(request, 'dashboard/blog_confirm_delete.html', context)

@admin_required
def blog_toggle_publish(request, pk):
    """Toggle blog publish status"""
    post = get_object_or_404(Post, pk=pk)
    post.is_published = not post.is_published
    if post.is_published and not post.published_at:
        post.published_at = timezone.now()
    post.save()
    status = "published" if post.is_published else "unpublished"
    messages.success(request, f'Blog post {status} successfully!')
    return redirect('dashboard:blog_list')


# ==================== CATEGORY MANAGEMENT ====================

@admin_required
def category_list(request):
    """List all categories"""
    categories = Category.objects.all()
    
    # Manually count posts for each category
    for category in categories:
        category.post_count = Post.objects.filter(category=category).count()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            import re
            slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            Category.objects.create(name=name, slug=slug)
            messages.success(request, f'Category "{name}" created successfully!')
            return redirect('dashboard:category_list')
    
    context = {
        'categories': categories,
        'active_page': 'categories',
    }
    return render(request, 'dashboard/category_list.html', context)

@admin_required
def category_create(request):
    """Create new category"""
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            import re
            slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            Category.objects.create(name=name, slug=slug)
            messages.success(request, f'Category "{name}" created successfully!')
        else:
            messages.error(request, 'Category name is required!')
        return redirect('dashboard:category_list')
    
    return redirect('dashboard:category_list')

@admin_required
def category_edit(request, pk):
    """Edit category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            import re
            category.name = name
            category.slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            category.save()
            messages.success(request, f'Category "{name}" updated successfully!')
        else:
            messages.error(request, 'Category name is required!')
        return redirect('dashboard:category_list')
    
    context = {'category': category, 'active_page': 'categories'}
    return render(request, 'dashboard/category_form.html', context)

@admin_required
def category_delete(request, pk):
    """Delete category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('dashboard:category_list')
    
    context = {'category': category}
    return render(request, 'dashboard/category_confirm_delete.html', context)


# ==================== TAG MANAGEMENT ====================

@admin_required
def tag_list(request):
    """List all tags"""
    tags = Tag.objects.all()
    
    # Manually count posts for each tag
    for tag in tags:
        tag.post_count = tag.posts.count()  # Note: 'posts' is the related_name from Post.tags
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            import re
            slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            Tag.objects.create(name=name, slug=slug)
            messages.success(request, f'Tag "{name}" created successfully!')
            return redirect('dashboard:tag_list')
    
    context = {
        'tags': tags,
        'active_page': 'tags',
    }
    return render(request, 'dashboard/tag_list.html', context)

@admin_required
def tag_create(request):
    """Create new tag"""
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            import re
            slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            Tag.objects.create(name=name, slug=slug)
            messages.success(request, f'Tag "{name}" created successfully!')
        else:
            messages.error(request, 'Tag name is required!')
        return redirect('dashboard:tag_list')
    
    return redirect('dashboard:tag_list')

@admin_required
def tag_edit(request, pk):
    """Edit tag"""
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            import re
            tag.name = name
            tag.slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            tag.save()
            messages.success(request, f'Tag "{name}" updated successfully!')
        else:
            messages.error(request, 'Tag name is required!')
        return redirect('dashboard:tag_list')
    
    context = {'tag': tag, 'active_page': 'tags'}
    return render(request, 'dashboard/tag_form.html', context)

@admin_required
def tag_delete(request, pk):
    """Delete tag"""
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag_name = tag.name
        tag.delete()
        messages.success(request, f'Tag "{tag_name}" deleted successfully!')
        return redirect('dashboard:tag_list')
    
    context = {'tag': tag}
    return render(request, 'dashboard/tag_confirm_delete.html', context)


from job.models import Job, JobCategory, JobApplication

# ==================== JOB MANAGEMENT ====================

@admin_required
def job_list(request):
    """List all jobs"""
    jobs = Job.objects.all().order_by('-created_at')
    
    # Search
    search = request.GET.get('search')
    if search:
        jobs = jobs.filter(title__icontains=search)
    
    # Filter by status
    status = request.GET.get('status')
    if status == 'active':
        jobs = jobs.filter(is_active=True)
    elif status == 'inactive':
        jobs = jobs.filter(is_active=False)
    
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'jobs': page_obj,
        'total_jobs': Job.objects.count(),
        'active_jobs': Job.objects.filter(is_active=True).count(),
        'inactive_jobs': Job.objects.filter(is_active=False).count(),
        'active_page': 'jobs',
    }
    return render(request, 'dashboard/job_list.html', context)

@admin_required
def job_create(request):
    """Create new job posting"""
    if request.method == 'POST':
        title = request.POST.get('title')
        if not title:
            messages.error(request, 'Title is required!')
            return redirect('dashboard:job_create')
        
        # Get or create category
        category_id = request.POST.get('category')
        category = None
        if category_id:
            category = JobCategory.objects.get(id=category_id)
        
        job = Job.objects.create(
            title=title,
            category=category,
            job_type=request.POST.get('job_type'),
            description=request.POST.get('description'),
            responsibilities=request.POST.get('responsibilities'),
            requirements=request.POST.get('requirements'),
            benefits=request.POST.get('benefits', ''),
            min_experience=request.POST.get('min_experience'),
            location=request.POST.get('location', 'Remote · Global'),
            salary_range=request.POST.get('salary_range', ''),
            is_active=request.POST.get('is_active') == 'on',
            featured=request.POST.get('featured') == 'on',
        )
        
        if request.FILES.get('icon'):
            job.icon = request.FILES['icon']
            job.save()
        
        messages.success(request, f'Job "{title}" created successfully!')
        return redirect('dashboard:job_list')
    
    categories = JobCategory.objects.all()
    context = {
        'categories': categories,
        'is_edit': False,
        'active_page': 'jobs',
    }
    return render(request, 'dashboard/job_form.html', context)

@admin_required
def job_edit(request, pk):
    """Edit existing job"""
    job = get_object_or_404(Job, pk=pk)
    
    if request.method == 'POST':
        job.title = request.POST.get('title')
        category_id = request.POST.get('category')
        job.category = JobCategory.objects.get(id=category_id) if category_id else None
        job.job_type = request.POST.get('job_type')
        job.description = request.POST.get('description')
        job.responsibilities = request.POST.get('responsibilities')
        job.requirements = request.POST.get('requirements')
        job.benefits = request.POST.get('benefits', '')
        job.min_experience = request.POST.get('min_experience')
        job.location = request.POST.get('location')
        job.salary_range = request.POST.get('salary_range', '')
        job.is_active = request.POST.get('is_active') == 'on'
        job.featured = request.POST.get('featured') == 'on'
        
        if request.FILES.get('icon'):
            job.icon = request.FILES['icon']
        
        job.save()
        messages.success(request, f'Job "{job.title}" updated successfully!')
        return redirect('dashboard:job_list')
    
    categories = JobCategory.objects.all()
    context = {
        'job': job,
        'categories': categories,
        'is_edit': True,
        'active_page': 'jobs',
    }
    return render(request, 'dashboard/job_form.html', context)

@admin_required
def job_delete(request, pk):
    """Delete job posting"""
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        job_title = job.title
        job.delete()
        messages.success(request, f'Job "{job_title}" deleted successfully!')
        return redirect('dashboard:job_list')
    
    context = {'job': job}
    return render(request, 'dashboard/job_confirm_delete.html', context)

@admin_required
def job_toggle_status(request, pk):
    """Toggle job active status"""
    job = get_object_or_404(Job, pk=pk)
    job.is_active = not job.is_active
    job.save()
    status = "activated" if job.is_active else "deactivated"
    messages.success(request, f'Job "{job.title}" {status}!')
    return redirect('dashboard:job_list')

# ==================== JOB APPLICATIONS MANAGEMENT ====================

@admin_required
def job_application_list(request):
    """List all job applications"""
    applications = JobApplication.objects.all().order_by('-created_at')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        applications = applications.filter(status=status)
    
    # Filter by job
    job_id = request.GET.get('job')
    if job_id:
        applications = applications.filter(job_id=job_id)
    
    # Search
    search = request.GET.get('search')
    if search:
        applications = applications.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    paginator = Paginator(applications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    jobs = Job.objects.all()
    
    context = {
        'applications': page_obj,
        'jobs': jobs,
        'total_applications': JobApplication.objects.count(),
        'pending_count': JobApplication.objects.filter(status='pending').count(),
        'shortlisted_count': JobApplication.objects.filter(status='shortlisted').count(),
        'hired_count': JobApplication.objects.filter(status='hired').count(),
        'active_page': 'applications',
    }
    return render(request, 'dashboard/job_application_list.html', context)

@admin_required
def job_application_detail(request, pk):
    """View single job application"""
    application = get_object_or_404(JobApplication, pk=pk)
    
    if request.method == 'POST':
        application.status = request.POST.get('status')
        application.notes = request.POST.get('notes')
        application.save()
        messages.success(request, 'Application status updated!')
        return redirect('dashboard:job_application_detail', pk=pk)
    
    context = {
        'application': application,
        'active_page': 'applications',
    }
    return render(request, 'dashboard/job_application_detail.html', context)

@admin_required
def job_application_delete(request, pk):
    """Delete job application"""
    application = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        application_name = application.full_name()
        application.delete()
        messages.success(request, f'Application from {application_name} deleted!')
        return redirect('dashboard:job_application_list')
    
    context = {'application': application}
    return render(request, 'dashboard/job_application_confirm_delete.html', context)

@admin_required
def job_application_update_status(request, pk):
    """Quick update application status"""
    application = get_object_or_404(JobApplication, pk=pk)
    new_status = request.GET.get('status')
    if new_status in dict(JobApplication.STATUS_CHOICES):
        application.status = new_status
        application.save()
        messages.success(request, f'Application status updated to {application.get_status_display()}!')
    return redirect('dashboard:job_application_detail', pk=pk)


# ==================== JOB CATEGORY MANAGEMENT ====================

@admin_required
def job_category_list(request):
    """List all job categories"""
    categories = JobCategory.objects.all().annotate(job_count=Count('jobs'))
    
    if request.method == 'POST':
        name = request.POST.get('name')
        icon = request.POST.get('icon', '')
        if name:
            import re
            slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            JobCategory.objects.create(name=name, slug=slug, icon=icon)
            messages.success(request, f'Category "{name}" created successfully!')
            return redirect('dashboard:job_category_list')
    
    context = {
        'categories': categories,
        'active_page': 'job_categories',
    }
    return render(request, 'dashboard/job_category_list.html', context)

@admin_required
def job_category_edit(request, pk):
    """Edit job category"""
    category = get_object_or_404(JobCategory, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            import re
            category.name = name
            category.slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            category.icon = request.POST.get('icon', '')
            category.save()
            messages.success(request, f'Category "{name}" updated successfully!')
            return redirect('dashboard:job_category_list')
    
    context = {'category': category, 'active_page': 'job_categories'}
    return render(request, 'dashboard/job_category_form.html', context)

@admin_required
def job_category_delete(request, pk):
    """Delete job category"""
    category = get_object_or_404(JobCategory, pk=pk)
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('dashboard:job_category_list')
    
    context = {'category': category}
    return render(request, 'dashboard/job_category_confirm_delete.html', context)

    # ==================== JOB CATEGORY MANAGEMENT ====================

@admin_required
def job_category_list(request):
    """List all job categories"""
    categories = JobCategory.objects.all().annotate(job_count=Count('jobs'))
    
    context = {
        'categories': categories,
        'active_page': 'job_categories',
    }
    return render(request, 'dashboard/job_category_list.html', context)

@admin_required
def job_category_create(request):
    """Create new job category"""
    if request.method == 'POST':
        name = request.POST.get('name')
        icon = request.POST.get('icon', '')
        if name:
            import re
            slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            JobCategory.objects.create(name=name, slug=slug, icon=icon)
            messages.success(request, f'Category "{name}" created successfully!')
            return redirect('dashboard:job_category_list')
        else:
            messages.error(request, 'Category name is required!')
    
    return redirect('dashboard:job_category_list')

@admin_required
def job_category_edit(request, pk):
    """Edit job category"""
    category = get_object_or_404(JobCategory, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            import re
            category.name = name
            category.slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            category.icon = request.POST.get('icon', '')
            category.save()
            messages.success(request, f'Category "{name}" updated successfully!')
            return redirect('dashboard:job_category_list')
        else:
            messages.error(request, 'Category name is required!')
    
    return redirect('dashboard:job_category_list')

@admin_required
def job_category_delete(request, pk):
    """Delete job category"""
    category = get_object_or_404(JobCategory, pk=pk)
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('dashboard:job_category_list')
    
    context = {'category': category}
    return render(request, 'dashboard/job_category_confirm_delete.html', context)