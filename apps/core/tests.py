from django.test import TestCase
from django.urls import reverse

PAGES = [
    ("core:home", "/", "pages/home.html"),
    ("core:about", "/sobre/", "pages/about.html"),
    ("core:programs", "/programas/", "pages/programs.html"),
    ("core:startups", "/startups/", "pages/startups.html"),
    ("core:contact", "/contato/", "pages/contact.html"),
]


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
                self.assertContains(
                    response,
                    f'class="main-nav__link is-active" href="{path}" aria-current="page"',
                    count=1,
                )

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
