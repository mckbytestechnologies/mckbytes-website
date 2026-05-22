from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import os

def job_image_upload_path(instance, filename):
    """Generate unique path for job images"""
    ext = filename.split('.')[-1]
    return f'jobs/{instance.slug}/icon.{ext}'

def resume_upload_path(instance, filename):
    """Generate unique path for resumes"""
    return f'resumes/{instance.job.slug}/{instance.first_name}_{instance.last_name}_{filename}'

class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font awesome icon class")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Job Categories"

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('contract', 'Contract'),
        ('part_time', 'Part-time'),
        ('internship', 'Internship'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    
    # Details
    description = models.TextField(help_text="Full job description")
    responsibilities = models.TextField(help_text="List responsibilities (one per line)")
    requirements = models.TextField(help_text="List requirements (one per line)")
    benefits = models.TextField(blank=True, help_text="List benefits (one per line)")
    
    # Meta
    min_experience = models.CharField(max_length=100, help_text="e.g., 1+ years, 3-5 years")
    location = models.CharField(max_length=200, default="Remote · Global")
    salary_range = models.CharField(max_length=100, blank=True)
    
    # Display
    icon = models.ImageField(upload_to=job_image_upload_path, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Job.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('jobs:job_detail', kwargs={'slug': self.slug})
    
    def get_responsibilities_list(self):
        return [r.strip() for r in self.responsibilities.split('\n') if r.strip()]
    
    def get_requirements_list(self):
        return [r.strip() for r in self.requirements.split('\n') if r.strip()]
    
    def get_benefits_list(self):
        return [b.strip() for b in self.benefits.split('\n') if b.strip()]
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    
    # Personal Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    
    # Professional Info
    years_experience = models.CharField(max_length=100)
    current_company = models.CharField(max_length=200, blank=True)
    current_role = models.CharField(max_length=200, blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    
    # Application
    cover_letter = models.TextField()
    resume = models.FileField(upload_to=resume_upload_path)
    additional_file = models.FileField(upload_to='additional/', blank=True, null=True)
    
    # Source
    source = models.CharField(max_length=100, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job.title}"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-created_at']

class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name