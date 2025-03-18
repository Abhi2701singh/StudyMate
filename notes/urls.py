from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-note/', views.add_note, name='add_note'),
    path('year/<int:year>/', views.year_notes, name='year_notes'),
    path('quantum/', views.quantum, name='quantum'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete-note/<int:note_id>/', views.delete_note, name='delete_note'),
] 