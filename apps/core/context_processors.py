from django.conf import settings

SITE = {
    "phone_display": "+(55) 64 3611 2200",
    "phone_footer": "(64) 3611 2200",
    "phone_href": "tel:+556436112200",
    "email": "ypetec@unirv.edu.br",
    "base": "UniRV, Rio Verde/GO",
    "legal": "Razão Social: FESURV - UNIVERSIDADE DE RIO VERDE CNPJ: 01.815.216/0001-78",
    "unirv_url": "https://www.unirv.edu.br/paginas.php?id=15#",
    "links": {
        "acesso_informacao": "https://acessoainformacao.unirv.edu.br/",
        "transparencia": "#",
        "ouvidoria": "http://www.unirv.edu.br/paginas.php",
        "fale_conosco": "http://www.unirv.edu.br/contato.php",
        "acessibilidade": "https://www.unirv.edu.br/paginas.php",
        "sei": "https://sei.unirv.edu.br/",
        "privacidade": "#",
        "entrar": "#",
    },
    # Links herdados do design no Figma (apontam para a Rádio UFG); trocar pelos perfis oficiais da Ypetec.
    "social": [
        {"name": "Instagram", "url": "https://www.instagram.com/radioufg/", "icon": "images/icons/social-instagram.svg", "width": 18, "height": 18},
        {"name": "Facebook", "url": "https://pt-br.facebook.com/radioufg/", "icon": "images/icons/social-facebook.svg", "width": 10, "height": 19},
        {"name": "YouTube", "url": "https://www.youtube.com/channel/UCVEN3bSdTJsYvDM0JfqerYA", "icon": "images/icons/social-youtube.svg", "width": 20, "height": 15},
        {"name": "WhatsApp", "url": "https://wa.me/556235211937", "icon": "images/icons/social-whatsapp.svg", "width": 18, "height": 18},
        {"name": "Rádio", "url": "https://radio.ufg.br/p/8051-radio-ao-vivo", "icon": "images/icons/social-radio.svg", "width": 20, "height": 19},
    ],
}

NAV_ITEMS = [
    ("home", "Início"),
    ("about", "Sobre"),
    ("programs", "Programas"),
    ("startups", "Startups", [
        ("startups", "Startups incubadas"),
        ("incubation", "Incubação"),
        ("calendar", "Calendário de funcionamento"),
    ]),
    ("contact", "Contato"),
]


# Páginas internas que destacam o item de menu de outra rota (etapas do formulário de incubação).
NAV_ALIASES = {"incubation_step2": "incubation", "incubation_step3": "incubation"}


def _nav_items(active):
    items = []
    for name, label, *rest in NAV_ITEMS:
        children = [
            {"route": f"core:{child}", "label": child_label, "active": child == active}
            for child, child_label in (rest[0] if rest else [])
        ]
        items.append({
            "name": name,
            "route": f"core:{name}",
            "label": label,
            "active": name == active or any(child["active"] for child in children),
            "children": children,
        })
    return items


def _asset_version():
    """Versão dos assets (mtime mais recente de CSS/JS) para invalidar o cache do navegador."""
    static = settings.BASE_DIR / "static"
    try:
        return int(max(f.stat().st_mtime for pattern in ("css/**/*.css", "js/**/*.js") for f in static.glob(pattern)))
    except (OSError, ValueError):
        return 0


def site(request):
    match = getattr(request, "resolver_match", None)
    active = match.url_name if match and match.namespace == "core" else None
    active = NAV_ALIASES.get(active, active)
    return {
        "site": SITE,
        "asset_version": _asset_version(),
        "nav_items": _nav_items(active),
    }
