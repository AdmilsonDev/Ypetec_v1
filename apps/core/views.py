import unicodedata
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from . import calendar_data, startups_data
from .forms import ContactForm
from .incubation_form import IncubationApplicationForm
from .incubation_planning_form import IncubationPlanningForm
from .incubation_startup_form import IncubationStartupForm


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


INCUBATION_STEPS = (
    "Informações do empreendedor responsável",
    "Informações da startup",
    "Planejamento para os próximos 3 anos",
)
INCUBATION_SESSION_KEY = "incubation_application"
INCUBATION_DONE_KEY = "incubation_submitted"


def _skip_incubation_validation():
    """TEMPORARIO: avanca de etapa sem validar (INCUBATION_SKIP_VALIDATION), para revisar o design."""
    return settings.INCUBATION_SKIP_VALIDATION


def _incubation_steps(current):
    return [
        {"number": number, "label": label, "state": "active" if number == current else "done" if number < current else ""}
        for number, label in enumerate(INCUBATION_STEPS, start=1)
    ]


def _json_safe(data):
    """Converte datas em texto para guardar os dados validados na sessão."""
    return {key: value.isoformat() if hasattr(value, "isoformat") else value for key, value in data.items()}


def _incubation_saved(request, step):
    return request.session.get(INCUBATION_SESSION_KEY, {}).get(f"step{step}")


def _incubation_save(request, step, form):
    data = request.session.get(INCUBATION_SESSION_KEY, {})
    skipped = getattr(form, "file_fields", ())
    data[f"step{step}"] = _json_safe({k: v for k, v in form.cleaned_data.items() if k not in skipped})
    request.session[INCUBATION_SESSION_KEY] = data


def incubation(request):
    """Etapa 1 - informações do empreendedor responsável."""
    if request.method == "POST":
        form = IncubationApplicationForm(request.POST)
        if form.is_valid() or _skip_incubation_validation():
            _incubation_save(request, 1, form)
            return redirect("core:incubation_step2")
    else:
        form = IncubationApplicationForm(initial=_incubation_saved(request, 1))
    return render(request, "pages/incubation.html", {"form": form, "steps": _incubation_steps(1)})


def incubation_step2(request):
    """Etapa 2 - informações da startup."""
    if _incubation_saved(request, 1) is None and not _skip_incubation_validation():
        return redirect("core:incubation")
    if request.method == "POST":
        form = IncubationStartupForm(request.POST)
        if form.is_valid() or _skip_incubation_validation():
            _incubation_save(request, 2, form)
            return redirect("core:incubation_step3")
    else:
        form = IncubationStartupForm(initial=_incubation_saved(request, 2))
    return render(request, "pages/incubation_step2.html", {"form": form, "steps": _incubation_steps(2)})


def incubation_step3(request):
    """Etapa 3 - planejamento para os próximos 3 anos; ao finalizar, a solicitação está completa."""
    if _incubation_saved(request, 2) is None and not _skip_incubation_validation():
        return redirect("core:incubation_step2")
    if request.method == "POST":
        form = IncubationPlanningForm(request.POST, request.FILES)
        if form.is_valid() or _skip_incubation_validation():
            _incubation_save(request, 3, form)
            # TODO: enviar a solicitação completa (etapas 1 a 3 + anexos) por e-mail/CRM quando o
            # destino estiver definido. Os anexos ainda não são armazenados.
            request.session[INCUBATION_DONE_KEY] = True  # abre o diálogo de conclusão após o redirect
            return redirect("core:incubation_step3")
    else:
        form = IncubationPlanningForm(initial=_incubation_saved(request, 3))
    return render(
        request,
        "pages/incubation_step3.html",
        {
            "form": form,
            "steps": _incubation_steps(3),
            "submitted": request.method == "GET" and request.session.pop(INCUBATION_DONE_KEY, False),
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
