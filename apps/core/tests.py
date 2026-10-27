from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

PAGES = [
    ("core:home", "/", "pages/home.html"),
    ("core:about", "/sobre/", "pages/about.html"),
    ("core:programs", "/programas/", "pages/programs.html"),
    ("core:startups", "/startups/", "pages/startups.html"),
    ("core:incubation", "/startups/incubacao/", "pages/incubation.html"),
    ("core:calendar", "/startups/calendario/", "pages/calendar.html"),
    ("core:contact", "/contato/", "pages/contact.html"),
]

# Páginas acessadas pelo submenu de "Startups".
SUBMENU_PATHS = {"/startups/", "/startups/calendario/", "/startups/incubacao/"}


class PublicPagesTests(TestCase):
    def test_pages_render(self):
        for name, path, template in PAGES:
            with self.subTest(name=name):
                self.assertEqual(reverse(name), path)
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "base.html")
                self.assertTemplateUsed(response, "layouts/public.html")
                self.assertTemplateUsed(response, template)

    def test_nav_marks_current_page(self):
        for name, path, _ in PAGES:
            with self.subTest(name=name):
                response = self.client.get(path)
                if path in SUBMENU_PATHS:
                    self.assertContains(
                        response,
                        f'class="main-nav__sublink is-active" href="{path}" aria-current="page"',
                        count=1,
                    )
                    self.assertContains(response, 'class="main-nav__link main-nav__toggle is-active"', count=1)
                else:
                    self.assertContains(
                        response,
                        f'class="main-nav__link is-active" href="{path}" aria-current="page"',
                        count=1,
                    )

    def test_startups_submenu_links_to_calendar(self):
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, 'aria-controls="nav-submenu-startups"')
        self.assertContains(response, 'href="/startups/calendario/"')
        self.assertContains(response, "Calendário de funcionamento")

    def test_home_has_no_temporary_figma_assets(self):
        response = self.client.get(reverse("core:home"))
        self.assertNotContains(response, "figma.com/api/mcp/asset")


class ContactFormTests(TestCase):
    url = "/contato/"
    valid = {
        "name": "Maria Luiza Alves",
        "phone": "(64) 9 8765-4321",
        "email": "maria@example.com",
        "subject": "Gostaria de conhecer os programas.",
        "consent": "on",
    }

    def test_valid_post_redirects_with_message(self):
        response = self.client.post(self.url, self.valid, follow=True)
        self.assertRedirects(response, self.url)
        self.assertContains(response, "Mensagem enviada")

    def test_invalid_email_shows_error(self):
        response = self.client.post(self.url, {**self.valid, "email": "esseemeuemail"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Insira um e-mail válido")

    def test_consent_and_required_fields(self):
        response = self.client.post(self.url, {})
        form = response.context["form"]
        self.assertEqual(set(form.errors), {"name", "email", "subject", "consent"})


class StartupsPageTests(TestCase):
    url = "/startups/"

    def test_lists_all_startups(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["page"].object_list), 9)
        self.assertContains(response, "Projetos que transformam")

    def test_search_ignores_case_and_accents(self):
        response = self.client.get(self.url, {"q": "AVIARIOS"})
        self.assertEqual([s["name"] for s in response.context["page"].object_list], ["PiuTech"])

    def test_category_filter(self):
        response = self.client.get(self.url, {"categoria": "Bebidas"})
        self.assertEqual([s["name"] for s in response.context["page"].object_list], ["TechBier"])

    def test_unknown_category_is_ignored(self):
        response = self.client.get(self.url, {"categoria": "Inexistente"})
        self.assertEqual(len(response.context["page"].object_list), 9)

    def test_empty_result_message(self):
        response = self.client.get(self.url, {"q": "zzz"})
        self.assertContains(response, "Nenhuma startup encontrada")


class CalendarPageTests(TestCase):
    url = "/startups/calendario/"

    def test_renders_six_months_of_second_semester(self):
        response = self.client.get(self.url)
        months = response.context["calendar_months"]
        self.assertEqual([m["name"] for m in months], ["Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
        self.assertContains(response, "Segundo semestre/2026")
        self.assertContains(response, 'class="calendar-month"', count=6)

    def test_weeks_start_on_sunday(self):
        # 1º de julho de 2026 é uma quarta-feira.
        july = self.client.get(self.url).context["calendar_months"][0]
        first_week = july["weeks"][0]
        self.assertEqual([c is None for c in first_week], [True, True, True, False, False, False, False])
        self.assertEqual(first_week[3]["number"], 1)

    def test_sundays_are_recess_and_holidays_marked(self):
        months = self.client.get(self.url).context["calendar_months"]
        july, sept = months[0], months[2]
        self.assertEqual(july["weeks"][1][0]["kind"], "recess")  # domingo, 5/7
        independence = next(c for w in sept["weeks"] for c in w if c and c["number"] == 7)
        self.assertEqual(independence["kind"], "holiday")
        self.assertIn("Independência", independence["label"])


@override_settings(INCUBATION_SKIP_VALIDATION=False)
class IncubationFormTests(TestCase):
    url = "/startups/incubacao/"
    valid = {
        "name": "Maria Luiza Alves",
        "cpf": "529.982.247-25",
        "birth_date": "1990-05-17",
        "nationality": "Brasileiro",
        "email": "maria@example.com",
        "phone": "(64) 9 8765-4321",
        "education": "superior",
        "address": "Rua das Flores, quadra 3, lote 4",
        "number": "123",
        "neighborhood": "Centro",
        "zip_code": "75901-970",
        "resume_url": "www.linkedin.com/in/maria",
        "role": "Sócia administradora",
        "dedication": "30 horas semanais",
    }

    def test_renders_stepper_and_fields(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Formulário de solicitação de incubação")
        self.assertContains(response, 'class="form-steps__item is-active" aria-current="step"', count=1)
        self.assertContains(response, 'class="ifield__control"', count=len(self.valid))

    def test_submenu_links_to_incubation(self):
        response = self.client.get("/")
        self.assertContains(response, 'href="/startups/incubacao/"')

    def test_valid_post_goes_to_step_two(self):
        response = self.client.post(self.url, self.valid)
        self.assertRedirects(response, "/startups/incubacao/etapa-2/")
        self.assertEqual(self.client.session["incubation_application"]["step1"]["birth_date"], "1990-05-17")

    def test_step_one_is_prefilled_from_session(self):
        self.client.post(self.url, self.valid)
        response = self.client.get(self.url)
        self.assertContains(response, 'value="Maria Luiza Alves"')

    def test_required_fields(self):
        response = self.client.post(self.url, {})
        self.assertEqual(set(response.context["form"].errors), set(self.valid))

    def test_invalid_cpf_and_future_birth_date(self):
        response = self.client.post(self.url, {**self.valid, "cpf": "111.111.111-11", "birth_date": "2999-01-01"})
        errors = response.context["form"].errors
        self.assertEqual(set(errors), {"cpf", "birth_date"})
        self.assertContains(response, "Informe um CPF válido.")

    def test_resume_url_gets_scheme(self):
        from .incubation_form import IncubationApplicationForm

        form = IncubationApplicationForm(self.valid)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["resume_url"], "https://www.linkedin.com/in/maria")


@override_settings(INCUBATION_SKIP_VALIDATION=False)
class IncubationStepTwoTests(TestCase):
    url = "/startups/incubacao/etapa-2/"
    valid = {
        "project_name": "AgroTech Rio Verde",
        "sector": "Agtech",
        "cnpj": "",
        "website": "",
        "problem": "Perdas na colheita.",
        "solution": "Sensor de umidade conectado.",
        "developed_by": "own_team",
        "stage": "prototyping",
        "idea_origin": "unmet_need",
        "has_patent": "no",
        "patent_number": "",
        "environmental_impact": "Não identificamos riscos.",
        "sdgs": ["2", "9"],
        "customers": "Produtores rurais.",
        "differentiation": "Menor custo.",
        "competitors": "Empresa A, B e C.",
        "value_proposition": "Redução de perdas.",
        "revenue_sources": "Assinatura mensal.",
        "business_items": ["investors"],
        "monthly_revenue": "0_1k",
        "recurring_revenue": "yes",
        "marketing_stage": "segmentation",
    }

    def _finish_step_one(self):
        self.client.post("/startups/incubacao/", IncubationFormTests.valid)

    def test_redirects_to_step_one_without_saved_data(self):
        self.assertRedirects(self.client.get(self.url), "/startups/incubacao/")

    def test_renders_with_step_two_active(self):
        self._finish_step_one()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/incubation_step2.html")
        self.assertContains(response, "form-steps--2")
        self.assertContains(response, 'class="form-steps__item is-done"', count=1)
        self.assertContains(response, 'class="form-steps__item is-active" aria-current="step"', count=1)
        self.assertContains(response, 'class="main-nav__sublink is-active" href="/startups/incubacao/" aria-current="page"')
        self.assertContains(response, "17 - Parcerias e meios de implementação")
        self.assertContains(response, "ypetec@unirv.edu.br</strong>")

    def test_valid_post_is_saved(self):
        self._finish_step_one()
        response = self.client.post(self.url, self.valid)
        self.assertRedirects(response, "/startups/incubacao/etapa-3/")
        self.assertEqual(self.client.session["incubation_application"]["step2"]["sdgs"], ["2", "9"])

    def test_required_fields(self):
        self._finish_step_one()
        errors = self.client.post(self.url, {}).context["form"].errors
        optional = {"cnpj", "website", "patent_number"}
        self.assertEqual(set(errors), set(self.valid) - optional)

    def test_patent_number_required_when_patent_is_yes(self):
        self._finish_step_one()
        response = self.client.post(self.url, {**self.valid, "has_patent": "yes"})
        self.assertEqual(set(response.context["form"].errors), {"patent_number"})

    def test_sdg_none_cannot_be_combined(self):
        self._finish_step_one()
        response = self.client.post(self.url, {**self.valid, "sdgs": ["none", "3"]})
        self.assertEqual(set(response.context["form"].errors), {"sdgs"})

    def test_cnpj_is_validated_when_given(self):
        self._finish_step_one()
        bad = self.client.post(self.url, {**self.valid, "cnpj": "11.111.111/1111-11"})
        self.assertEqual(set(bad.context["form"].errors), {"cnpj"})
        good = self.client.post(self.url, {**self.valid, "cnpj": "11.222.333/0001-81"})
        self.assertEqual(good.status_code, 302)


@override_settings(INCUBATION_SKIP_VALIDATION=False)
class IncubationStepThreeTests(TestCase):
    url = "/startups/incubacao/etapa-3/"
    valid = {
        "year_one": "Validar o produto com 20 clientes.",
        "year_two": "Expandir para três estados.",
        "year_three": "Buscar investimento série A.",
        "attended_event": "yes",
        "was_incubated": "no",
        "expectations": "Mentoria e acesso a pesquisadores.",
        "found_out": "Pelo Instagram da YpeTec.",
    }

    def _finish_step_two(self):
        session = self.client.session
        session["incubation_application"] = {"step1": {}, "step2": {}}
        session.save()

    def test_redirects_without_step_two(self):
        self.assertRedirects(
            self.client.get(self.url), "/startups/incubacao/etapa-2/", fetch_redirect_response=False
        )

    def test_renders_with_step_three_active(self):
        self._finish_step_two()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/incubation_step3.html")
        self.assertContains(response, "form-steps--3")
        self.assertContains(response, 'enctype="multipart/form-data"')
        self.assertContains(response, "Finalizar")
        self.assertNotContains(response, 'id="incubation-done"')

    def test_required_fields(self):
        self._finish_step_two()
        response = self.client.post(self.url, {})
        self.assertEqual(set(response.context["form"].errors), set(self.valid))
        self.assertNotContains(response, 'id="incubation-done"')

    def test_valid_post_is_saved_without_files(self):
        self._finish_step_two()
        upload = SimpleUploadedFile("plano.pdf", b"%PDF-1.4 teste", content_type="application/pdf")
        response = self.client.post(self.url, {**self.valid, "attachment_1": upload}, follow=True)
        self.assertRedirects(response, self.url)
        self.assertContains(response, 'id="incubation-done"')
        self.assertContains(response, "Muito bom, você finalizou")
        # o diálogo aparece só uma vez
        self.assertNotContains(self.client.get(self.url), 'id="incubation-done"')
        saved = self.client.session["incubation_application"]["step3"]
        self.assertEqual(saved["attended_event"], "yes")
        self.assertNotIn("attachment_1", saved)

    def test_rejects_unsupported_attachment(self):
        self._finish_step_two()
        upload = SimpleUploadedFile("virus.exe", b"MZ", content_type="application/octet-stream")
        response = self.client.post(self.url, {**self.valid, "attachment_2": upload})
        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment_2", response.context["form"].errors)


@override_settings(INCUBATION_SKIP_VALIDATION=True)
class IncubationSkipValidationTests(TestCase):
    """Modo temporário de revisão de design: avança as etapas sem validar."""

    def test_step_one_advances_with_empty_form(self):
        self.assertRedirects(self.client.post("/startups/incubacao/", {}), "/startups/incubacao/etapa-2/")

    def test_step_two_opens_without_step_one(self):
        self.assertEqual(self.client.get("/startups/incubacao/etapa-2/").status_code, 200)

    def test_step_two_accepts_empty_form(self):
        self.assertRedirects(self.client.post("/startups/incubacao/etapa-2/", {}), "/startups/incubacao/etapa-3/")

    def test_step_three_accepts_empty_form(self):
        response = self.client.post("/startups/incubacao/etapa-3/", {}, follow=True)
        self.assertContains(response, 'id="incubation-done"')
