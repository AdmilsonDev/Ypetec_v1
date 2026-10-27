"""Dados do Calendário de funcionamento (segundo semestre).

Para marcar datas, edite os dicionários abaixo:

* ``HOLIDAYS``: feriados (quadrado azul na legenda "Feriado");
* ``EVENTS``: eventos (quadrado vermelho na legenda "Evento");
* ``RECESS_DATES``: recessos (número verde, "Recesso"). Os domingos já são
  tratados como recesso automaticamente.

Quando uma data aparece em mais de uma categoria, vale a prioridade
feriado > evento > recesso.
"""

import calendar
from datetime import date

YEAR = 2026
MONTHS = (7, 8, 9, 10, 11, 12)
TITLE = "Segundo semestre"

MONTH_NAMES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}

# (letra exibida, nome completo) com a semana iniciando no domingo.
WEEKDAYS = (
    ("D", "Domingo"),
    ("S", "Segunda-feira"),
    ("T", "Terça-feira"),
    ("Q", "Quarta-feira"),
    ("Q", "Quinta-feira"),
    ("S", "Sexta-feira"),
    ("S", "Sábado"),
)

HOLIDAYS = {
    date(2026, 9, 7): "Independência do Brasil",
    date(2026, 10, 12): "Nossa Senhora Aparecida",
    date(2026, 11, 2): "Finados",
    date(2026, 11, 15): "Proclamação da República",
    date(2026, 11, 20): "Consciência Negra",
    date(2026, 12, 25): "Natal",
}

EVENTS: dict[date, str] = {}

RECESS_DATES: dict[date, str] = {}

LEGEND = (
    ("recess", "Recesso"),
    ("holiday", "Feriado"),
    ("event", "Evento"),
)

KIND_LABELS = {"recess": "Recesso", "holiday": "Feriado", "event": "Evento"}


def _kind(day: date) -> tuple[str, str]:
    if day in HOLIDAYS:
        return "holiday", HOLIDAYS[day]
    if day in EVENTS:
        return "event", EVENTS[day]
    if day in RECESS_DATES:
        return "recess", RECESS_DATES[day]
    if day.weekday() == 6:
        return "recess", ""
    return "", ""


def build_months() -> list[dict]:
    """Monta os meses do semestre, com a semana começando no domingo."""
    cal = calendar.Calendar(firstweekday=6)
    months = []
    for month in MONTHS:
        weeks = []
        for week in cal.monthdayscalendar(YEAR, month):
            cells = []
            for number in week:
                if not number:
                    cells.append(None)
                    continue
                kind, note = _kind(date(YEAR, month, number))
                label = KIND_LABELS.get(kind, "")
                if label and note:
                    label = f"{label}: {note}"
                cells.append({"number": number, "kind": kind, "label": label})
            weeks.append(cells)
        months.append({"name": MONTH_NAMES[month], "year": YEAR, "weeks": weeks})
    return months
