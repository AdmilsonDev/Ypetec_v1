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
    ("startups", "Startups"),
    ("contact", "Contato"),
]


def site(request):
    match = getattr(request, "resolver_match", None)
    active = match.url_name if match and match.namespace == "core" else None
    return {
        "site": SITE,
        "nav_items": [
            {"route": f"core:{name}", "label": label, "active": name == active}
            for name, label in NAV_ITEMS
        ],
    }
