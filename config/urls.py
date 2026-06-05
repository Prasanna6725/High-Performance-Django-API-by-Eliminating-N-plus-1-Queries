from django.contrib import admin
from django.urls import path, re_path

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^healthz/?$', views.healthz),
    re_path(r'^api/posts/naive/?$', views.naive_posts),
    re_path(r'^api/posts/optimized/?$', views.optimized_posts),
    re_path(r'^api/posts/advanced/?$', views.advanced_posts),
]
