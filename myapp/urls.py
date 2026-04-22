from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/', views.all_projects, name='all_projects'),
    path('subject/<int:pk>/', views.subject_detail, name='subject_detail'),
    path('material/<int:pk>/', views.material_detail, name='material_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('verify/<str:token>/', views.verify_email_action, name='verify_email'),
    path('create-admin/', create_temp_admin),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)