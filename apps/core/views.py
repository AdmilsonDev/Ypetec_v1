import unicodedata
from urllib.parse import urlencode

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from . import calendar_data, startups_data
from .forms import ContactForm


def home(request):
    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/about.html")


def programs(request):
    return render(request, "pages/programs.html")


def _fold(text):
    """Minúsculas e sem acentos, para a busca."""
    return "".join(c for c in unicodedata.normalize("NFD", text.casefold()) if not unicodedata.combining(c))


def startups(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("categoria", "").strip()
    if category not in startups_data.categories():
        category = ""

    items = startups_data.STARTUPS
    if category:
        items = [s for s in items if s["category"] == category]
    if query:
        needle = _fold(query)
        items = [s for s in items if needle in _fold(f"{s['name']} {s['description']}")]

    page = Paginator(items, startups_data.PER_PAGE).get_page(request.GET.get("page"))
    filters = {key: value for key, value in (("q", query), ("categoria", category)) if value}
    return render(
        request,
        "pages/startups.html",
        {
            "page": page,
            "query": query,
            "category": category,
            "categories": startups_data.categories(),
            "filter_query": urlencode(filters),
        },
    )


def calendar_page(request):
    return render(
        request,
        "pages/calendar.html",
        {
            "calendar_title": calendar_data.TITLE,
            "calendar_year": calendar_data.YEAR,
            "calendar_legend": calendar_data.LEGEND,
            "calendar_weekdays": calendar_data.WEEKDAYS,
            "calendar_months": calendar_data.build_months(),
        },
    )


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
