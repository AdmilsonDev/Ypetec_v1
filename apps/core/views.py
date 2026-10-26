from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm


def home(request):
    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/about.html")


def programs(request):
    return render(request, "pages/programs.html")


def startups(request):
    return render(request, "pages/startups.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # TODO: encaminhar a mensagem (e-mail/CRM) quando o destino estiver definido.
            messages.success(request, "Mensagem enviada! Retornaremos em breve.")
            return redirect("core:contact")
    else:
        form = ContactForm()
    return render(request, "pages/contact.html", {"form": form})
