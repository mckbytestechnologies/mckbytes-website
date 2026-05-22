from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import JobCategory, Job, JobApplication

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'job_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def job_count(self, obj):
        return obj.jobs.filter(is_active=True).count()
    job_count.short_description = 'Active Jobs'

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'job_type', 'location', 'is_active', 'featured', 'application_count', 'created_at']
    list_filter = ['category', 'job_type', 'is_active', 'featured', 'location']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_active', 'featured']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'job_type', 'location', 'min_experience', 'salary_range')
        }),
        ('Job Description', {
            'fields': ('description', 'responsibilities', 'requirements', 'benefits'),
            'classes': ('wide',)
        }),
        ('Display Settings', {
            'fields': ('icon', 'is_active', 'featured'),
            'classes': ('wide',)
        }),
    )
    
    def application_count(self, obj):
        count = obj.applications.count()
        url = reverse('admin:jobs_jobapplication_changelist') + f'?job__id__exact={obj.id}'
        return format_html('<a href="{}">{} applications</a>', url, count)
    application_count.short_description = 'Applications'

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'job', 'years_experience', 'status', 'created_at', 'view_resume_link']
    list_filter = ['job', 'status', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['mark_as_reviewed', 'mark_as_shortlisted', 'mark_as_rejected', 'mark_as_hired']
    
    fieldsets = (
        ('Job & Status', {
            'fields': ('job', 'status', 'notes')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'location')
        }),
        ('Professional Information', {
            'fields': ('years_experience', 'current_company', 'current_role', 'linkedin_url', 'portfolio_url')
        }),
        ('Application', {
            'fields': ('cover_letter', 'resume', 'additional_file', 'source')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'
    
    def view_resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank" style="background:#C8102E; color:#fff; padding:4px 12px; border-radius:4px; text-decoration:none;">📄 View Resume</a>', obj.resume.url)
        return '-'
    view_resume_link.short_description = 'Resume'
    
    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
    mark_as_reviewed.short_description = "Mark as Reviewed"
    
    def mark_as_shortlisted(self, request, queryset):
        queryset.update(status='shortlisted')
    mark_as_shortlisted.short_description = "Mark as Shortlisted"
    
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_as_rejected.short_description = "Mark as Rejected"
    
    def mark_as_hired(self, request, queryset):
        queryset.update(status='hired')
    mark_as_hired.short_description = "Mark as Hired"