"""yt_a URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from yt_site import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # slash after port number is not considered here.Start writing stuff which follows it.
    path('', views.home, name='home'),#For first page,ip:port/
    path('page/<page_number>', views.home, name='home'),
    # path('^image/(\d+)',views.image_serve,name='image_serve') #When img src="/image/hash"
    path('image/<hash_of_image>',views.image_serve,name='image_serve'),#hash_of_image keyword args
    path('upload/',views.upload_file,name='upload_file'),
    path('search/',views.search,name='search')
    ]
