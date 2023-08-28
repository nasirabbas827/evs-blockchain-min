from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='home'),
    path('elections/', views.election_list, name='election_list'),
    path('register/', views.custom_register, name='register'),  # Custom user registration view
    path('login/', views.custom_login, name='login'),            # Custom login view
    path('logout/', views.custom_logout, name='logout'),         # Custom logout view
    path('election/<int:election_id>/', login_required(views.election_detail), name='election_detail'),
    path('election/<int:election_id>/results/', views.view_results, name='view_results'),
    path('update_profile/', views.update_profile, name='update_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
