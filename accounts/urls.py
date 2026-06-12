from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.custom_signup, name='account_signup'),
    path('settings/', views.settings_view, name='settings'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('account/delete/', views.account_delete_view, name='account_delete'),
    path('change-theme/', views.change_theme, name='change_theme'),
]

