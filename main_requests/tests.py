from django.test import TestCase

# Create your tests here.
# Такой тест нужен для каждой страницы чтобы убедится что все view отрабатывают без ошибок!!
# Если в таких тестах ошибка - view при запросе в браузере выкенет code 500 instead, which means Internal Server Error.
from django.urls import resolve, reverse
from .views import home, new_request, filter_requests


class testMainPage(TestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    # Тест на соответствие пути и view
    # путь / возвращает	view name = 'home' прописана в urls.py результат функции home(request)
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class testNewMainRequest(TestCase):
    def setUp(self):
        url = reverse('new_request')
        self.response = self.client.get(url)

    def test_new_request_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_new_url_resolves_new_view(self):
        view = resolve('/new_request/')
        self.assertEquals(view.func, new_request)


class testFilterMainRequest(TestCase):
    def setUp(self):
        url = reverse('filter_request')
        self.response = self.client.get(url)

    def test_new_request_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_new_url_resolves_new_view(self):
        view = resolve('/filter_request/')
        self.assertEquals(view.func, filter_requests)
