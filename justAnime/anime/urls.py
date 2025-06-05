from django.urls import path
from . import views


urlpatterns = [
    path('', views.anime_list, name='anime_list'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('<slug:slug>/add_comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('add/', views.add_anime, name='add_anime'),
    path('<slug:slug>/edit/', views.edit_anime, name='edit_anime'),
    path('<slug:slug>/delete/', views.delete_anime, name='delete_anime'),
    path('<slug:slug>/', views.anime_detail, name='anime_detail'),
    path('<slug:slug>/progress/', views.update_progress, name='update_progress'),
    path('accounts/profile/', views.accounts_profile_redirect),
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
