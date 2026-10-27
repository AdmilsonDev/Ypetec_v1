from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("sobre/", views.about, name="about"),
    path("programas/", views.programs, name="programs"),
    path("startups/", views.startups, name="startups"),
    path("startups/calendario/", views.calendar_page, name="calendar"),
    path("startups/incubacao/", views.incubation, name="incubation"),
    path("startups/incubacao/etapa-2/", views.incubation_step2, name="incubation_step2"),
    path("startups/incubacao/etapa-3/", views.incubation_step3, name="incubation_step3"),
    path("contato/", views.contact, name="contact"),
]
