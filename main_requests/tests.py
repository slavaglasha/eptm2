from django.test import TestCase
# Create your tests here.
# Такой тест нужен для каждой страницы чтобы убедится что все view отрабатывают без ошибок!!
# Если в таких тестах ошибка - view при запросе в браузере выкенет code 500 instead, which means Internal Server Error.
from django.urls import resolve, reverse

from main_requests.models import MainRequest
from main_requests.testss.createtrestBase import createBase, createDepartments, createGroups, createUsers
from .views import test_base, ListFilterJsonView


class testMainPage(TestCase):
    @classmethod
    def setUpTestData(cls):
        createDepartments()
        createUsers()
        createGroups()

    def setUp(self):
        print('testMainPage')
        url = reverse('view')
        self.response = self.client.get(url)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('view'))
        self.assertRedirects(resp, '/login/?next=/')

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        self.client.login(username='user1', password='12345')
        resp = self.client.get(reverse('view'))

        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/login/'))

    def test_logged_in_with_permission_staus_code(self):
        self.client.login(username='user1', password='11223344')
        resp = self.client.get(reverse('view'))
        # Check that it lets us login -
        self.assertEqual(resp.status_code, 200)

    # Тест на соответствие пути поумолчанию для залогиненого пользователя и view
    def test_loged_in_with_permission_staus_code(self):
        self.client.login(username='user1', password='11223344')
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
class testFilterMainRequest(TestCase):
    @classmethod
    def setUpTestData(cls):
        createDepartments()
        createUsers()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('list_json'))
        self.assertRedirects(resp, '/need_login/?next=/test2/filter-request-json/')

    def test_new_request_status_code(self):
        self.client.login(username='user1', password='11223344')
        url = reverse('list_json')
        self.response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)

    def test_new_url_resolves_new_view(self):
        self.client.login(username='user1', password='11223344')
        url = reverse('list_json')
        self.response = self.client.get(url)
        view = resolve('/test2/filter-request-json/')
        self.assertEquals(view.func, ListFilterJsonView)




class testUpdateMainRequest(TestCase):
    @classmethod
    def setUpTestData(cls):
        MainRequest.objects.all().delete()
        createDepartments()
        createUsers()
        createBase()

    def test_mainrequest_success_status_code(self):
        self.client.login(username='user1', password='11223344')
        m1 = MainRequest.objects.all()
        print(m1[0].id)
        url = reverse('base_update_veiw', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_absolute_url(self):
        url = reverse('base_update_veiw', kwargs={'pk': 1})
        # This will also fail if the urlconf is not defined.
        self.assertEquals(url, '/base/update-request/1/')

    def test_mainrequest_notfound_status_code(self):
        self.client.login(username='user1', password='11223344')
        url = reverse('base_update_veiw', kwargs={'pk': 10})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_mainrequest_if_not_logged_in(self):
        resp = self.client.get(reverse('base_update_veiw', kwargs={'pk': 1}))
        self.assertRedirects(resp, '/need_login/?next=/base/update-request/1/')
