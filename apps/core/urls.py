from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("sobre/", views.about, name="about"),
    path("programas/", views.programs, name="programs"),
    path("startups/", views.startups, name="startups"),
    path("startups/calendario/", views.calendar_page, name="calendar"),
    path("contato/", views.contact, name="contact"),
]
