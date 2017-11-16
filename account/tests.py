from django.test import TestCase

# Create your tests here.
from django.urls import reverse, resolve
from .views import signup


class testSignUp(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_new_signup_resolves_new_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

class tetsLogIn(TestCase):
    def setUp(self):
        url = reverse('login')
        self.response = self.client.get(url)

    def test_login_status_code(self):
        self.assertEquals(self.response.status_code, 200)

