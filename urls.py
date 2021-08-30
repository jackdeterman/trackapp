"""trackapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('load_spreadsheet', views.load_spreadsheet, name="load_spreadsheet"),
    path("", views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path("user_list", views.user_list, name="user_list"), 
    path('profile/<int:user_id>', views.profile, name="profile"),
    path('meets', views.meets, name="meets"),
    path('meet/<int:meet_id>', views.meet, name="meet"),
    path('events', views.events, name="events"),
    path('event/<int:event_id>', views.event, name="event"),
    path('add_result/<int:user_id>', views.add_result, name="add_result"),
    path('edit_profile/<int:user_id>', views.edit_profile, name="edit_profile"),
    path('edit_result/<int:result_id>', views.edit_result, name="edit_result"),
    path('search', views.search, name="search"),
    path('merge_athlete/<int:user_id>', views.merge_athlete, name="merge_athlete"),
    path('delete_result/<int:result_id>', views.delete_result, name="delete_result")
]
