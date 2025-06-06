"""personalWebpage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from personalWebpage import views
from literature import views as literature_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login_user/', auth_views.LoginView.as_view(), name='login_user'),
    path('logout_user/', auth_views.LogoutView.as_view(), name='logout_user'),
    path('', include('frontpage.urls')),
    path('about/', include('about.urls')),
    path('foundationResponse/', include('foundationResponse.urls')),
    path('literature/', include('literature.urls')),
    path('logged_in/', views.logged_in, name='logged_in'),
    path('airflow/', include('airflow.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)