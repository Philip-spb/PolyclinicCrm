from django.test import TestCase
from .models import Doctors, Orders
from datetime import date as d
from datetime import timedelta


class ViewsTestCase(TestCase):
    doctor = Doctors()

    def setUp(self):
        # Создаем нового доктора
        self.doctor = Doctors.objects.create(name='Иванов Иван Иванович')
        self.doctor.save()

    def test_approval(self):
        date = d.today()
        redirect = '/'
        patient_name = 'Семён'

        # Проверяем что при указании несущесьтвующего доктора мы никуда не перенаправляемся
        response = self.client.post(redirect, {'doctor': '2'}, follow=True)
        self.assertEqual(response.redirect_chain, [])

        # Производим выбор лечащего врача
        response = self.client.post(redirect, {'doctor': self.doctor.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        redirect = response.redirect_chain[0][0]

        # Производим выбор даты для бронирования
        if date.weekday() in [5, 6]:
            date += timedelta(days=2)

        response = self.client.post(redirect,
                                    {'date_day': date.day,
                                     'date_month': date.month,
                                     'date_year': date.year},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        redirect = response.redirect_chain[0][0]

        # Проверяем наличие перенаправления при указании неверного временного периода
        response = self.client.post(str(redirect) + '3/', {'patient': patient_name}, follow=True)
        self.assertTrue(response.redirect_chain)

        # Бронируем конкретное время
        response = self.client.post(str(redirect) + '10/', {'patient': patient_name}, follow=True)
        self.assertEqual(response.status_code, 200)

        # Проверяем, создался ли заказ
        self.assertEqual(Orders.objects.last().patient, patient_name)

        # Пробуем забронировать время которое уже у врача занято (получаем редирект)
        response = self.client.post(str(redirect) + '10/', {'patient': patient_name}, follow=True)
        self.assertTrue(response.redirect_chain)
