from django.db import models


class Doctors(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя врача')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'


class Orders(models.Model):
    date = models.DateField(verbose_name='Дата')
    time_period = models.IntegerField(verbose_name='Зарезервированное время')
    patient = models.CharField(max_length=255, verbose_name='Имя пациента')
    doctor = models.ForeignKey(Doctors, on_delete=models.PROTECT, related_name='orders', verbose_name='Имя врача')

    def __str__(self):
        return str(self.date) + ' – ' + str(self.time_period) + ':00' + ' – ' + str(self.patient)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
