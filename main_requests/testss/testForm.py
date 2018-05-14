from django.test import TestCase
from django.urls import reverse

from main_requests.filter import MainRequestFilter
from main_requests.models import MainRequest


class testFilterForm(TestCase):
    def setUp(self):
        self.url = reverse('list_json')
        self.response = self.client.get(self.url,follow=True)
        self.filter = MainRequestFilter(self.response, queryset=MainRequest.objects.all().order_by('-pk')[0:1])
        self.form = self.filter.form

    def test_field_label(self):
        self.assertTrue(
            self.form.fields['number'].label is None or self.form.fields['number'].label == '№')
        self.assertEqual(
           self.form.fields['input_datetime'].label , 'Дата вводда')
        self.assertEqual(
            self.form.fields['input_user'].label, 'Пользователь')
        self.assertEqual(
            self.form.fields['request_dateTime'].label, 'Дата подачи заявки')
        self.assertEqual(
            self.form.fields['request_user'].label, 'Подал')

        self.assertEqual(
            self.form.fields['receive_dateTime'].label, 'Дата принятия')
        self.assertEqual(
            self.form.fields['receive_user'].label, 'Принял')
        self.assertEqual(
            self.form.fields['close_dateTime'].label, 'Дата закрытия')
        self.assertEqual(
            self.form.fields['close_user'].label, 'Закрыл')
        self.assertEqual(
           self.form.fields['place'].label, 'Место')
        self.assertEqual(self.form.fields['request_user'].help_text,'Можно ввести с клавиатуры')

    def test_form_number(self):
        number = 'qqw'
        form_data = {'input_datetime': number}
        resp = self.client.get(self.url,form_data,follow=True)
        filter = MainRequestFilter(resp, queryset=MainRequest.objects.all().order_by('-pk')[0:1])
        form = filter.form
        self.assertFalse(form.is_valid())

