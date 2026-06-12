from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/members/', views.project_members, name='project_members'),
    path('projects/<int:pk>/members/<int:member_id>/remove/', views.project_delete_member, name='delete_member'),

    path('projects/<int:project_pk>/tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/status/', views.update_task_status, name='update_task_status'),
    path('tasks/my/', views.my_tasks, name='my_tasks'),

    path('tasks/<int:task_pk>/comments/', views.add_comment, name='add_comment'),
    path('comments/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),

    path('legal/terms/', views.terms_of_service, name='terms_of_service'),
    path('legal/privacy/', views.privacy_policy, name='privacy_policy'),
    path('legal/contact/', views.contact_us, name='contact_us'),
    path('legal/about/', views.about_us, name='about_us'),
    path('legal/blog/', views.blog, name='blog'),
]
