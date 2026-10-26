from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/about.html")


def programs(request):
    return render(request, "pages/programs.html")


def startups(request):
    return render(request, "pages/startups.html")


def contact(request):
    return render(request, "pages/contact.html")
