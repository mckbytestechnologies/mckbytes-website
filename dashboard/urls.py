from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Authentication
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    
    # Dashboard Home
    path('', views.dashboard_home, name='dashboard_home'),
    
    # Contact Management
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    
    # Blog Management
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    path('blog/<int:pk>/toggle-publish/', views.blog_toggle_publish, name='blog_toggle_publish'),
    
    # Category Management
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Tag Management
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/create/', views.tag_create, name='tag_create'),
    path('tags/<int:pk>/edit/', views.tag_edit, name='tag_edit'),
    path('tags/<int:pk>/delete/', views.tag_delete, name='tag_delete'),

    # Job Management
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('jobs/<int:pk>/toggle-status/', views.job_toggle_status, name='job_toggle_status'),

    # Job Applications
    path('applications/', views.job_application_list, name='job_application_list'),
    path('applications/<int:pk>/', views.job_application_detail, name='job_application_detail'),
    path('applications/<int:pk>/delete/', views.job_application_delete, name='job_application_delete'),
    path('applications/<int:pk>/update-status/', views.job_application_update_status, name='job_application_update_status'),

    # Job Categories
    path('job-categories/', views.job_category_list, name='job_category_list'),
    path('job-categories/create/', views.job_category_create, name='job_category_create'),  # ← ADD THIS LINE
    path('job-categories/<int:pk>/edit/', views.job_category_edit, name='job_category_edit'),
    path('job-categories/<int:pk>/delete/', views.job_category_delete, name='job_category_delete'),
]