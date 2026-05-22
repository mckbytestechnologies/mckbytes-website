from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.careers_page, name='careers'),
    path('apply/', views.apply_job, name='apply_job'),
]