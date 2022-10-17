"""mini_ups URL Configuration

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
import django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from deliveries import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('logout/', django.contrib.auth.views.logout, {'next_page': 'home'}, name='logout'),
    path('accounts/home/', views.account_package_tracking),
    path('packages/edit/<int:package_id>', views.package_edit),
    path('packages/detail/<int:tracking_number>', views.package_view_with_id),
    path('packages/detail/', views.package_view),
    path('packages/create/', views.package_create),
    path('accounts/ups/create/', views.ups_account_create)
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
