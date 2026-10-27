from django import forms
from django.core.exceptions import ValidationError

from .incubation_form import _digits

DEVELOPED_BY = [("own_team", "Equipe própria"), ("third_parties", "Terceiros")]

STAGES = [
    ("ideation", "Ideação"),
    ("prototyping", "Prototipação"),
    ("mvp", "MVP validado no mercado"),
    ("operating", "Atuando"),
]

IDEA_ORIGINS = [
    ("unmet_need", "De percepção de uma necessidade de mercado, ainda não atendida"),
    (
        "poorly_served_need",
        "Da percepção de uma necessidade de mercado, que não está sendo satisfatoriamente atendida "
        "pelas empresas existentes.",
    ),
    ("affinity", "Da vontade em empreender em uma área que possui afinidade."),
]

YES_NO = [("yes", "Sim"), ("no", "Não")]

SDG_NONE = "none"
SDGS = [
    ("1", "1 - Erradicação da pobreza"),
    ("2", "2 - Fome zero e agricultura sustentável"),
    ("3", "3 - Saúde e bem-estar"),
    ("4", "4 - Educação de qualidade"),
    ("5", "5 - Igualdade de gênero"),
    ("6", "6 - Água potável e saneamento"),
    ("7", "7 - Energia limpa e acessível"),
    ("8", "8 - Trabalho decente e crescimento econômico"),
    ("9", "9 - Indústria, inovação e infraestrutura"),
    ("10", "10 - Redução das desigualdades"),
    ("11", "11 - Cidades e comunidades sustentáveis"),
    ("12", "12 - Consumo e produção sustentável"),
    ("13", "13 - Ação contra a mudança global do clima"),
    ("14", "14 - Vida na água"),
    ("15", "15 - Vida terrestre"),
    ("16", "16 - Paz, justiça e instituições eficazes"),
    ("17", "17 - Parcerias e meios de implementação"),
    (SDG_NONE, "Não atuamos em nenhum dos objetivos"),
]

BUSINESS_ITEMS = [
    ("founders_subsistence", "Os empreendedores contam com recursos financeiros para subsistência"),
    ("finish_product", "A empresa conta com recursos para terminar o desenvolvimento do produto"),
    ("market_actions", "A empresa conta com recursos financeiros para executar ações de mercado"),
    ("break_even", "A empresa conta com recursos para tocar o negócio até o ponto de equilíbrio"),
    ("investors", "A empresa obteve recursos de investidores"),
    ("grants", "A empresa obteve recursos de fomento (FINEP, CNPq, OUTROS)"),
]

MONTHLY_REVENUE = [
    ("0_1k", "R$ 0 a R$ 1.000"),
    ("1k_5k", "R$ 1.001 a R$ 5.000"),
    ("5k_10k", "R$ 5.001 a R$ 10.000"),
    ("10k_50k", "R$ 10.001 a R$ 50.000"),
    ("50k_plus", "Acima de R$ 50.000"),
]

MARKETING_STAGES = [
    ("segmentation", "Segmentação de mercado definida"),
    ("positioning", "Posicionamento de marca definido"),
    ("market_size", "Tamanho de mercado definido"),
    ("channels", "Canais de comunicação e vendas definidos"),
    ("sales_process", "Processos de vendas estruturados"),
    ("sales_delivered", "Vendas realizadas e produto/serviço sendo entregues"),
    ("in_use", "Produto/serviço comercializado em uso em clientes"),
]


def validate_cnpj(value: str) -> None:
    cnpj = _digits(value)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        raise ValidationError("Informe um CNPJ válido.")
    for size in (12, 13):
        weights = ([5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2] if size == 12 else [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        total = sum(int(d) * w for d, w in zip(cnpj[:size], weights))
        check = 0 if total % 11 < 2 else 11 - total % 11
        if check != int(cnpj[size]):
            raise ValidationError("Informe um CNPJ válido.")


def _text(placeholder, **attrs):
    return forms.TextInput(attrs={"placeholder": placeholder, **attrs})


def _area(placeholder="Discorra", rows=3):
    return forms.Textarea(attrs={"placeholder": placeholder, "rows": rows})


def _radio(label, choices, message):
    return forms.ChoiceField(
        label=label,
        choices=choices,
        widget=forms.RadioSelect,
        error_messages={"required": message, "invalid_choice": "Selecione uma opção válida."},
    )


def _checks(label, choices, message):
    return forms.MultipleChoiceField(
        label=label,
        choices=choices,
        widget=forms.CheckboxSelectMultiple,
        error_messages={"required": message, "invalid_choice": "Selecione opções válidas."},
    )


def _long(label, message, max_length=3000, rows=3):
    return forms.CharField(
        label=label, max_length=max_length, error_messages={"required": message}, widget=_area(rows=rows)
    )


class IncubationStartupForm(forms.Form):
    """Etapa 2 do formulário de solicitação de incubação: informações da startup."""

    project_name = forms.CharField(
        label="Nome do empreendimento",
        max_length=150,
        error_messages={"required": "Informe o nome do empreendimento."},
        widget=_text("Nome do empreendimento"),
    )
    sector = forms.CharField(
        label="Área/Setor de atuação",
        max_length=100,
        error_messages={"required": "Informe a área ou setor de atuação."},
        widget=_text("Tecnologia"),
    )
    cnpj = forms.CharField(
        label="CNPJ (caso tenha)",
        max_length=18,
        required=False,
        validators=[validate_cnpj],
        widget=_text("00.000.000/0000-00", inputmode="numeric"),
    )
    website = forms.URLField(
        label="URL Site (caso tenha)",
        required=False,
        assume_scheme="https",
        max_length=300,
        error_messages={"invalid": "Informe um link válido."},
        widget=_text("www.exemplo.com.br", inputmode="url", autocomplete="url"),
    )
    problem = _long(
        "Qual problema ou necessidade sua empresa quer resolver? Por que você escolheu esse problema?",
        "Descreva o problema ou necessidade.",
        rows=8,
    )
    solution = _long(
        "Qual a solução concedida? Ressalte funcionalidades e aplicações que caracterizam inovação",
        "Descreva a solução.",
        rows=8,
    )
    developed_by = _radio("A solução foi/será desenvolvida por:", DEVELOPED_BY, "Selecione uma opção.")
    stage = _radio("Qual o atual estágio de desenvolvimento da sua solução?", STAGES, "Selecione o estágio atual.")
    idea_origin = _radio("A ideia do negócio surgiu a partir de:", IDEA_ORIGINS, "Selecione uma opção.")
    has_patent = _radio("O produto, serviço ou processo possui patente?", YES_NO, "Selecione uma opção.")
    patent_number = forms.CharField(
        label="Se sim, informe o número do processo de patente ou protocolo:",
        max_length=100,
        required=False,
        widget=_text("Insira"),
    )
    environmental_impact = _long(
        "O produto, serviço ou processo pode gerar impactos/riscos de agressões ao meio ambiente?",
        "Responda sobre os impactos ao meio ambiente.",
    )
    sdgs = _checks(
        "Seu negócio atua em algum dos 17 Objetivos de Desenvolvimento Sustentável? Se sim, qual (ais)?",
        SDGS,
        "Selecione ao menos uma opção.",
    )
    customers = _long("Quem são os seus usuários e/ou clientes?", "Descreva seus usuários e/ou clientes.")
    differentiation = _long(
        "Como a sua solução se diferencia das concorrentes?", "Descreva os diferenciais da solução."
    )
    competitors = _long(
        "Quais os seus concorrentes atualmente? Quem pode vir a ser no futuro? "
        "(Cite os três principais concorrentes para seu negócio).",
        "Cite os principais concorrentes.",
    )
    value_proposition = _long(
        "Qual a sua proposta de valor? Qual o principal benefício percebido pelos clientes na solução?",
        "Descreva a proposta de valor.",
    )
    revenue_sources = _long("Qual (ais) as suas fontes de receitas?", "Informe as fontes de receita.")
    business_items = _checks(
        "Assinale os itens que se aplicam ao seu negócio:", BUSINESS_ITEMS, "Selecione ao menos uma opção."
    )
    monthly_revenue = _radio(
        "ATUALMENTE, qual a sua média de receita mensal com a solução?",
        MONTHLY_REVENUE,
        "Selecione a faixa de receita mensal.",
    )
    recurring_revenue = _radio("O modelo de receita é/será recorrente?", YES_NO, "Selecione uma opção.")
    marketing_stage = _radio(
        "Qual o estágio de desenvolvimento das ações do marketing?",
        MARKETING_STAGES,
        "Selecione o estágio das ações de marketing.",
    )

    #: campos exibidos como grupos de opções (radio/checkbox); os demais são texto
    choice_fields = {
        "developed_by", "stage", "idea_origin", "has_patent", "sdgs",
        "business_items", "monthly_revenue", "recurring_revenue", "marketing_stage",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            attrs = field.widget.attrs
            attrs["class"] = "choice__input" if name in self.choice_fields else "ifield__control"
            if field.required:
                attrs["required"] = True
            attrs["aria-describedby"] = f"{name}-error"
            if self.is_bound and name in self.errors:
                attrs["aria-invalid"] = "true"

    def clean_sdgs(self):
        selected = self.cleaned_data["sdgs"]
        if SDG_NONE in selected and len(selected) > 1:
            raise ValidationError("Não combine \"Não atuamos em nenhum dos objetivos\" com outros objetivos.")
        return selected

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("has_patent") == "yes" and not (cleaned.get("patent_number") or "").strip():
            self.add_error("patent_number", "Informe o número do processo de patente ou protocolo.")
        return cleaned
