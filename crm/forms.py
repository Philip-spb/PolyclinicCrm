from datetime import datetime

from django import forms
from .models import Doctors


class DoctorsForm(forms.Form):
    """
    Форма выбора лечашего врача
    """
    doctor = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': "form-select mb-2"}),
        required=True,
        queryset=Doctors.objects.all(),
        empty_label=None,
        label='Выбор лечащего врача')


class DateForm(forms.Form):
    """
    Форма выбора даты для записи
    """
    date = forms.DateField(
        label='Дата',
        widget=forms.SelectDateWidget(attrs={'class': "form-select mb-2"}),
        required=True,
        initial=datetime.now()
    )


class CustomersForm(forms.Form):
    """
    Форма записи ФИО клиента
    """
    patient = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control mb-2"}),
        required=True,
        label='Введите ваше имя')