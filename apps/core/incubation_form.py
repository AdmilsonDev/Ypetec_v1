import re
from datetime import date

from django import forms
from django.core.exceptions import ValidationError

EDUCATION_CHOICES = [
    ("", "Escolha..."),
    ("fundamental", "Ensino fundamental"),
    ("medio", "Ensino médio"),
    ("tecnico", "Ensino técnico"),
    ("superior_incompleto", "Superior incompleto"),
    ("superior", "Superior completo"),
    ("especializacao", "Especialização / MBA"),
    ("mestrado", "Mestrado"),
    ("doutorado", "Doutorado"),
]


def _digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def validate_cpf(value: str) -> None:
    cpf = _digits(value)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValidationError("Informe um CPF válido.")
    for size in (9, 10):
        total = sum(int(d) * w for d, w in zip(cpf[:size], range(size + 1, 1, -1)))
        check = (total * 10 % 11) % 10
        if check != int(cpf[size]):
            raise ValidationError("Informe um CPF válido.")


def validate_birth_date(value: date) -> None:
    if value > date.today():
        raise ValidationError("A data de nascimento não pode estar no futuro.")
    if value.year < 1900:
        raise ValidationError("Informe uma data de nascimento válida.")


def validate_phone(value: str) -> None:
    if len(_digits(value)) not in (10, 11):
        raise ValidationError("Informe um telefone com DDD.")


def validate_zip(value: str) -> None:
    if len(_digits(value)) != 8:
        raise ValidationError("Informe um CEP válido.")


def _text(placeholder, **attrs):
    return forms.TextInput(attrs={"placeholder": placeholder, **attrs})


class IncubationApplicationForm(forms.Form):
    """Etapa 1 do formulário de solicitação de incubação: dados do empreendedor responsável."""

    name = forms.CharField(
        label="Nome empreendedor responsável",
        max_length=150,
        error_messages={"required": "Informe o nome completo."},
        widget=_text("Nome Completo", autocomplete="name"),
    )
    cpf = forms.CharField(
        label="CPF do(a) solicitante",
        max_length=14,
        validators=[validate_cpf],
        error_messages={"required": "Informe o CPF."},
        widget=_text("000.000.000-00", inputmode="numeric"),
    )
    birth_date = forms.DateField(
        label="Data de nascimento",
        validators=[validate_birth_date],
        error_messages={"required": "Informe a data de nascimento.", "invalid": "Informe uma data válida."},
        widget=forms.DateInput(attrs={"type": "date", "autocomplete": "bday"}, format="%Y-%m-%d"),
    )
    nationality = forms.CharField(
        label="Nacionalidade",
        max_length=60,
        error_messages={"required": "Informe a nacionalidade."},
        widget=_text("Brasileiro"),
    )
    email = forms.EmailField(
        label="E-mail",
        error_messages={"required": "Informe o e-mail.", "invalid": "Insira um e-mail válido"},
        widget=forms.EmailInput(attrs={"placeholder": "email@email.com.br", "autocomplete": "email"}),
    )
    phone = forms.CharField(
        label="Telefone",
        max_length=20,
        validators=[validate_phone],
        error_messages={"required": "Informe o telefone."},
        widget=forms.TextInput(
            attrs={"placeholder": "(00) 0 0000-0000", "autocomplete": "tel", "inputmode": "tel", "type": "tel"}
        ),
    )
    education = forms.ChoiceField(
        label="Escolaridade",
        choices=EDUCATION_CHOICES,
        error_messages={"required": "Selecione a escolaridade.", "invalid_choice": "Selecione uma opção válida."},
    )
    address = forms.CharField(
        label="Endereço",
        max_length=200,
        error_messages={"required": "Informe o endereço."},
        widget=_text("Rua, avenida, quadra e lote", autocomplete="street-address"),
    )
    number = forms.CharField(
        label="Número",
        max_length=20,
        error_messages={"required": "Informe o número."},
        widget=_text("Número"),
    )
    neighborhood = forms.CharField(
        label="Bairro",
        max_length=100,
        error_messages={"required": "Informe o bairro."},
        widget=_text("Bairro"),
    )
    zip_code = forms.CharField(
        label="CEP",
        max_length=9,
        validators=[validate_zip],
        error_messages={"required": "Informe o CEP."},
        widget=_text("00000-000", autocomplete="postal-code", inputmode="numeric"),
    )
    resume_url = forms.URLField(
        label="Link para currículo on-line",
        assume_scheme="https",
        max_length=300,
        error_messages={"required": "Informe o link do currículo.", "invalid": "Informe um link válido."},
        widget=_text("www.linkedin.com.br", inputmode="url", autocomplete="url"),
    )
    role = forms.CharField(
        label="Função na empresa",
        max_length=100,
        error_messages={"required": "Informe a função na empresa."},
        widget=_text("Ex.: Sócio(a) administrador(a)"),
    )
    dedication = forms.CharField(
        label="Quanto tempo terá para se dedicar ao negócio?",
        max_length=100,
        error_messages={"required": "Informe o tempo de dedicação."},
        widget=_text("0 horas"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            attrs = field.widget.attrs
            attrs["class"] = "ifield__control"
            attrs["required"] = True
            attrs["aria-describedby"] = f"{name}-error"
            if self.is_bound and name in self.errors:
                attrs["aria-invalid"] = "true"
