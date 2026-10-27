"""Startups incubadas exibidas em /startups/.

Cada item: nome, categoria, descrição, logo (relativo a static/) e o tamanho de
exibição da logo dentro do cartão. ``photo=True`` indica imagem que preenche todo
o quadro (sem logo centralizada).
"""

STARTUPS = [
    {
        "name": "PiuTech",
        "category": "Agronegócio",
        "description": "Monitoramento e controle de aviários via IoT e IA.\nMaximizando a eficiência e a rentabilidade da sua produção.",
        "logo": "images/startups/logo-piutech.svg",
        "logo_width": 212,
        "logo_height": 65,
    },
    {
        "name": "Connect Mudas",
        "category": "Agronegócio",
        "description": "Plataforma digital para conectar produtores rurais que precisam reflorestar áreas degradadas a viveiros",
        "logo": "images/startups/logo-connect-mudas.png",
        "logo_width": 140,
        "logo_height": 137,
    },
    {
        "name": "Heliora",
        "category": "Tecnologia",
        "description": "Desenvolve soluções para o setor odontológico",
        "logo": "images/startups/logo-heliora.svg",
        "logo_width": 184,
        "logo_height": 139,
    },
    {
        "name": "Implemen. Conect",
        "category": "Software",
        "description": "Sistema integrado que monitora máquinas e implementos agrícolas por meio de sensores de vibração.",
        "logo": "images/startups/logo-implemen-conect.png",
        "logo_width": 194,
        "logo_height": 81,
    },
    {
        "name": "Secagem digital",
        "category": "Software",
        "description": "O projeto propõe a criação de um sistema digital capaz de monitorar, em tempo real, variáveis críticas do processo de secagem",
        "logo": "images/startups/logo-secagem-digital.png",
        "logo_width": 221,
        "logo_height": 92,
    },
    {
        "name": "Grou Bots",
        "category": "Tecnologia",
        "description": "Tem como seu principal produto um ROVER/ROBÔ (Veículo Elétrico Autônomo) Agrícola para o manejo de culturas agrícola",
        "logo": "images/startups/logo-grou-bots.png",
        "logo_width": 180,
        "logo_height": 92,
    },
    {
        "name": "Futura Drone",
        "category": "Tecnologia",
        "description": "É dedicada ao desenvolvimento e aplicação de soluções com aeronaves remotamente pilotadas para o setor agrícola",
        "logo": "images/startups/logo-futura-drone.png",
        "logo_width": 161,
        "logo_height": 122,
    },
    {
        "name": "TechBier",
        "category": "Bebidas",
        "description": "É uma microfábrica modular para produção de cerveja artesanal, composta por três módulos integráveis",
        "logo": "images/startups/logo-techbier.jpg",
        "logo_width": 269,
        "logo_height": 186,
        "photo": True,
    },
    {
        "name": "Silobot",
        "category": "Software",
        "description": "O SiloBot é um robô projetado para operar dentro de silos de grão.",
        "logo": "images/startups/logo-silobot.png",
        "logo_width": 155,
        "logo_height": 111,
    },
]

PER_PAGE = 9


def categories():
    return sorted({s["category"] for s in STARTUPS})
