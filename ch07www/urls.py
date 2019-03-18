"""ch07www URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from mysite import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('filer/', include('filer.urls')),
    path('', views.index),
    path('detail/<int:id>', views.detail, name = 'detail-url'),
    path('<int:pid>/<str:del_pass>', views.index),
    path('list/', views.listing),
    path('post/', views.posting),
    path('contact/', views.contact),
    path('post2db/', views.post2db),
    path('captcha/', include('captcha.urls')),
    path('login/', views.login),
    path('logout/', views.logout),
    path('userinfo/', views.userinfo),
    path('diarypost/', views.diarypost),
    path('accounts/', include('registration.backends.default.urls')),
    path('leveltwoinfo/', views.leveltwoinfo),
    path('leveltwoinfo/<int:del_key>/<str:del_product>', views.leveltwoinfo),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEIDA_ROOT)

