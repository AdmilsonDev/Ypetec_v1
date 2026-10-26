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
