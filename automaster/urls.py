"""URL configuration for automaster project.The `urlpatterns` list routes URLs to views. For more information please see:    https://docs.djangoproject.com/en/5.1/topics/http/urls/Examples:Function views    1. Add an import:  from my_app import views    2. Add a URL to urlpatterns:  path('', views.home, name='home')Class-based views    1. Add an import:  from other_app.views import Home    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')Including another URLconf    1. Import the include() function: from django.urls import include, path    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from service.views import home
from django.urls import path
from service import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [    path('', home, name='home'),    
               path('login/', LoginView.as_view(template_name='login.html'), name='login'),   
                 path('logout/', LogoutView.as_view(), name='logout'),    
                 path('about/', views.about, name='about'),    
                 path('price/', views.price_list, name='price'),    
                 path('contacts/', views.contacts, name='contacts'),    
                 path('cabinet/', views.cabinet, name='cabinet'),    
                 path('appointment/', views.create_appointment, name='appointment'),    
                 path('admin-panel/', views.admin_panel, name='admin_panel'),    
                 path('approve/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),    
                 path('reject/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),    
                 path('django-admin/', admin.site.urls, name='admin'),  ]

if settings.DEBUG:    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)