from django.test import TestCase
from django.urls import reverse

PAGES = [
    ("core:home", "/", "pages/home.html"),
    ("core:about", "/sobre/", "pages/about.html"),
    ("core:programs", "/programas/", "pages/programs.html"),
    ("core:startups", "/startups/", "pages/startups.html"),
    ("core:calendar", "/startups/calendario/", "pages/calendar.html"),
    ("core:contact", "/contato/", "pages/contact.html"),
]

# Páginas acessadas pelo submenu de "Startups".
SUBMENU_PATHS = {"/startups/", "/startups/calendario/"}


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
