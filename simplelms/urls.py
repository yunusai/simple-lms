"""
URL configuration for simplelms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]


urlpatterns += [
    path('statistics/users-with-courses/', views.users_with_courses_count, name='users_with_courses_count'),
    path('statistics/users-without-courses/', views.users_without_courses_count, name='users_without_courses_count'),
    path('statistics/avg-courses-followed/', views.avg_courses_followed, name='avg_courses_followed'),
    path('statistics/top-course-follower/', views.top_course_follower, name='top_course_follower'),
    path('statistics/users-not-following/', views.users_not_following_courses, name='users_not_following_courses'),
]