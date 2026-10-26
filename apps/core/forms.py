from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Nome completo",
        max_length=120,
        error_messages={"required": "Informe seu nome completo."},
        widget=forms.TextInput(attrs={"placeholder": "Maria Luiza Alves", "autocomplete": "name"}),
    )
    phone = forms.CharField(
        label="Telefone",
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "(DDD) 9 8765-4321", "autocomplete": "tel", "inputmode": "tel", "type": "tel"}
        ),
    )
    email = forms.EmailField(
        label="E-mail",
        error_messages={
            "required": "Informe seu e-mail.",
            "invalid": "Insira um e-mail válido",
        },
        widget=forms.EmailInput(attrs={"placeholder": "nome@exemplo.com", "autocomplete": "email"}),
    )
    subject = forms.CharField(
        label="Assunto",
        max_length=2000,
        error_messages={"required": "Escreva o assunto da sua mensagem."},
        widget=forms.Textarea(attrs={"placeholder": "Gostaria de...", "rows": 4}),
    )
    consent = forms.BooleanField(
        required=True,
        error_messages={"required": "É necessário concordar com os termos para enviar."},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            attrs = field.widget.attrs
            attrs["class"] = "check__input" if name == "consent" else "field__control"
            if field.required:
                attrs["required"] = True
                attrs["aria-describedby"] = f"{name}-error"
            if self.is_bound and name in self.errors:
                attrs["aria-invalid"] = "true"
