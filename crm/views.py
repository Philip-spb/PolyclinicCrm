from django.contrib import messages
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404

from .forms import DoctorsForm, DateForm, CustomersForm
from .models import Doctors, Orders


def doctor_approval(request):
    if request.method == 'POST':
        form = DoctorsForm(request.POST)
        if form.is_valid():
            return redirect('date_approval', request.POST['doctor'])
    else:
        form = DoctorsForm()
    return render(request, 'crm/doctor_approval.html', {'form': form})


def date_approval(request, doctor):
    approve_doctor = get_object_or_404(Doctors, pk=doctor)
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            day = int(request.POST['date_day'])
            month = int(request.POST['date_month'])
            year = int(request.POST['date_year'])

            if date(year, month, day) < date.today():
                messages.error(request, 'Вы указали неверную дату. Пройдите процесс заново.')
                return redirect('date_approval', doctor)

            if date(year, month, day).weekday() in [5, 6]:
                messages.error(request, 'В субботу и воскресенье доктора не принимают.')
                return redirect('date_approval', doctor)

            ord_date = date(year, month, day).toordinal()
            return redirect('time_approval', approve_doctor.pk, ord_date)
    else:
        form = DateForm()
    return render(request, 'crm/date_approval.html', {'doctor': approve_doctor, 'form': form})


def time_approval(request, doctor, ord_date):
    approve_doctor = get_object_or_404(Doctors, pk=doctor)
    approve_date = date.fromordinal(ord_date)

    if approve_date < date.today():
        messages.error(request, 'Вы указали неверную дату. Пройдите процесс заново.')
        return redirect('date_approval', doctor)

    if approve_date.weekday() in [5, 6]:
        messages.error(request, 'В субботу и воскресенье доктора не принимают.')
        return redirect('date_approval', doctor)

    orders = [order.time_period for order in approve_doctor.orders.filter(date=approve_date)]
    all_time = [time for time in range(9, 18)]

    free_time = dict()

    for time in all_time:
        if time in orders:
            free_time[time] = 1
        else:
            free_time[time] = 0

    params = {'doctor': approve_doctor, 'date': approve_date, 'free_time': free_time, 'ord_date': ord_date}
    return render(request, 'crm/time_approval.html', params)


def final_approval(request, doctor, ord_date, period):
    approve_doctor = get_object_or_404(Doctors, pk=doctor)
    approve_date = date.fromordinal(ord_date)

    if approve_date < date.today():
        messages.error(request, 'Вы указали неверную дату. Пройдите процесс заново.')
        return redirect('date_approval', doctor)

    if approve_date.weekday() in [5, 6]:
        messages.error(request, 'В субботу и воскресенье доктора не принимают.')
        return redirect('date_approval', doctor)

    if not 8 < period < 19:
        messages.error(request, 'Вы пытаетесь забронировать нерабочее время. Пройдите процесс заново.')
        return redirect('time_approval', doctor, ord_date)

    if Orders.objects.filter(date=approve_date, time_period=period, doctor=approve_doctor):
        messages.error(request, 'Этот период более недоступен для бронирования. Пройдите процесс заново.')
        return redirect('time_approval', doctor, ord_date)

    if request.method == 'POST':
        form = CustomersForm(request.POST)
        if form.is_valid():
            order = Orders.objects.create(date=approve_date,
                                          time_period=period,
                                          patient=request.POST['patient'],
                                          doctor=approve_doctor)
            order.save()

            params = {
                'doctor': approve_doctor,
                'date': approve_date,
                'period': period,
                'patient': request.POST['patient'],
                'order': order.pk}

            return render(request, 'crm/confirmation.html', params)
    else:
        form = CustomersForm()

    params = {'doctor': approve_doctor, 'date': approve_date, 'period': period, 'ord_date': ord_date, 'form': form}
    return render(request, 'crm/final_approval.html', params)
