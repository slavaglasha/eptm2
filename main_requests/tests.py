from django.test import TestCase

# Create your tests here.
# Такой тест нужен для каждой страницы чтобы убедится что все view отрабатывают без ошибок!!
# Если в таких тестах ошибка - view при запросе в браузере выкенет code 500 instead, which means Internal Server Error.
from django.urls import resolve, reverse
from .views import test_base, CreateNewRequest, ListFilterJsonView
from django.contrib.auth.models import User, Group  # Required to assign User as a borrower


def createGroups():
    group1 = Group.objects.create(name='Администрато')
    group1.save()
    group2 = Group.objects.create(name='Исполнитель')
    group2.save()
    group3 = Group.objects.create(name='Пользователи')
    group3.save()


def createUsers():
    user1 = User.objects.create_user(username='user1', password='11223344')
    user1.save()
    user2 = User.objects.create_user(username='user2', password='11223344')
    user2.save()


class testMainPage(TestCase):
    def setUp(self):
        url = reverse('view')
        self.response = self.client.get(url)
        createUsers()
        createGroups()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('view'))
        self.assertRedirects(resp, '/login/?next=/')

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='user1', password='12345')
        resp = self.client.get(reverse('view'))

        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/login/'))

    def test_logged_in_with_permission_staus_code(self):
        login = self.client.login(username='user1', password='11223344')
        resp = self.client.get(reverse('view'))

        # Check that it lets us login - this is our book and we have the right permissions.
        self.assertEqual(resp.status_code, 200)

    # Тест на соответствие пути поумолчанию для залогиненого пользователя и view
    def test_logged_in_with_permission_staus_code(self):
        login = self.client.login(username='user1', password='11223344')
        view = resolve('/')
        # Check that it lets us login - this is our book and we have the right permissions.
        self.assertEquals(view.func, test_base)

#
#
#         # def test_home_view_status_code(self):
#         #     self.assertEquals(self.response.status_code, 200)
#
#         # Тест на соответствие пути и view
#         # путь / возвращает	view name = 'home' прописана в urls.py результат функции home(request)
#         # def test_home_url_resolves_home_view(self):
#         #     view = resolve('/')
#         #     self.assertEquals(view.func, home)
#
#
# class testNewMainRequest(TestCase):
#     def setUp(self):
#         createUsers()
#
#     def test_redirect_if_not_logged_in(self):
#         resp = self.client.get(reverse('base_create_view'))
#         self.assertRedirects(resp, '/login')
#
#     def test_redirect_if_logged_in_but_not_correct_permission(self):
#         login = self.client.login(username='user1', password='12345')
#         resp = self.client.get(reverse('base_create_view'))
#
#         # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
#         self.assertEqual(resp.status_code, 302)
#         self.assertTrue(resp.url.startswith('/login/'))
#
#     def setloginCorrect(self):
#         login = self.client.login(username='user1', password='11223344')
#         url = reverse('base_create_view')
#         self.response = self.client.get(url)
#
#     def test_new_request_status_code(self):
#         self.setloginCorrect()
#         self.assertEquals(self.response.status_code, 200)
#
#     def test_new_url_resolves_new_view(self):
#         self.setloginCorrect()
#         view = resolve('/new_request/')
#         self.assertEquals(view.func, CreateNewRequest)
#
#
# class testFilterMainRequest(TestCase):
#     def setUp(self):
#
#         createUsers()
#
#     def test_new_request_status_code(self):
#
#         login = self.client.login(username='user1', password='11223344')
#         url = reverse('filter_request')
#         self.response = self.client.get(url)
#         self.assertEquals(self.response.status_code, 200)
#
#     def test_new_url_resolves_new_view(self):
#         login = self.client.login(username='user1', password='11223344')
#         url = reverse('filter_request')
#         self.response = self.client.get(url)
#         view = resolve('/test2/filter-request-json/')
#         self.assertEquals(view.func, ListFilterJsonView)
