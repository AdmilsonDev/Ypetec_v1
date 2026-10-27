from django import forms
from django.core.exceptions import ValidationError

from .incubation_startup_form import YES_NO, _area, _long, _radio

ATTACHMENT_MAX_MB = 10
ATTACHMENT_EXTENSIONS = (".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".png", ".jpg", ".jpeg")


def _attachment_label(number):
    return f"Anexo {number}"


class IncubationPlanningForm(forms.Form):
    """Etapa 3 do formulário de solicitação de incubação: planejamento para os próximos 3 anos."""

    year_one = _long("Primeiro ano", "Descreva o planejamento do primeiro ano.", rows=8)
    year_two = _long("Segundo ano", "Descreva o planejamento do segundo ano.", rows=8)
    year_three = _long("Terceiro ano", "Descreva o planejamento do terceiro ano.", rows=8)
    attended_event = _radio("Você já participou de algum evento da YpeTec?", YES_NO, "Selecione uma opção.")
    was_incubated = _radio("Já participou de algum processo de incubação?", YES_NO, "Selecione uma opção.")
    expectations = _long(
        "O que você(s) espera(m) do relacionamento do Empreendimento com a YpeTec?",
        "Descreva suas expectativas.",
        rows=4,
    )
    found_out = forms.CharField(
        label="Como ficou sabendo do edital?",
        max_length=3000,
        error_messages={"required": "Informe como ficou sabendo do edital."},
        widget=_area(rows=4),
    )
    attachment_1 = forms.FileField(label=_attachment_label(1), required=False)
    attachment_2 = forms.FileField(label=_attachment_label(2), required=False)

    #: campos exibidos como grupos de opções (radio); os demais são texto
    choice_fields = {"attended_event", "was_incubated"}
    #: arquivos enviados não são guardados na sessão
    file_fields = ("attachment_1", "attachment_2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            attrs = field.widget.attrs
            if name in self.file_fields:
                attrs["class"] = "upload__input"
                attrs["accept"] = ",".join(ATTACHMENT_EXTENSIONS)
            else:
                attrs["class"] = "choice__input" if name in self.choice_fields else "ifield__control"
            if field.required:
                attrs["required"] = True
            attrs["aria-describedby"] = f"{name}-error"
            if self.is_bound and name in self.errors:
                attrs["aria-invalid"] = "true"

    def _clean_attachment(self, name):
        upload = self.cleaned_data.get(name)
        if not upload:
            return upload
        if not upload.name.lower().endswith(ATTACHMENT_EXTENSIONS):
            raise ValidationError("Formato de arquivo não aceito. Envie PDF, Office ou imagem.")
        if upload.size > ATTACHMENT_MAX_MB * 1024 * 1024:
            raise ValidationError(f"O arquivo deve ter no máximo {ATTACHMENT_MAX_MB} MB.")
        return upload

    def clean_attachment_1(self):
        return self._clean_attachment("attachment_1")

    def clean_attachment_2(self):
        return self._clean_attachment("attachment_2")
