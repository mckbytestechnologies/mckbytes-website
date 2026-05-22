from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Job, JobApplication

def careers_page(request):
    jobs = Job.objects.filter(is_active=True)
    context = {
        'jobs': jobs,
        'total_jobs': jobs.count(),
        'current_year': 2025,
    }
    return render(request, 'careers.html', context)

def apply_job(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        
        application = JobApplication.objects.create(
            job=job,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            location=request.POST.get('location'),
            years_experience=request.POST.get('years_experience'),
            current_company=request.POST.get('current_company', ''),
            current_role=request.POST.get('current_role', ''),
            linkedin_url=request.POST.get('linkedin_url', ''),
            portfolio_url=request.POST.get('portfolio_url', ''),
            cover_letter=request.POST.get('cover_letter'),
            source=request.POST.get('source', ''),
        )
        
        if request.FILES.get('resume'):
            application.resume = request.FILES['resume']
        if request.FILES.get('additional_file'):
            application.additional_file = request.FILES['additional_file']
        application.save()
        
        messages.success(request, 'Your application has been submitted successfully! We will review it within 5 business days.')
        return redirect('jobs:careers')
    
    return redirect('jobs:careers')