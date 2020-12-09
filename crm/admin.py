from datetime import date

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Doctors, Orders


class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    fields = ('name', 'order_list')
    readonly_fields = ('order_list',)

    def order_list(self, obj):
        orders = Orders.objects.filter(doctor=obj.id).order_by('date','time_period')
        order_str = ''
        # Показываем только актуальные бронирования
        for order in orders:
            if order.date >= date.today():
                order_str += str(order) + '<br>'
        return mark_safe(order_str)

    order_list.short_description = 'Список бронирований'


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'date', 'period', 'patient',)
    list_display_links = ('id', 'doctor', 'date',)
    search_fields = ('doctor', 'patient',)
    fields = ('doctor', 'date', 'time_period', 'patient',)
    readonly_fields = ('period',)
    list_filter = ('doctor', 'date')

    def period(self, obj):
        if obj.time_period:
            return mark_safe(f'{obj.time_period}:00 – {obj.time_period+1}:00')

    period.short_description = 'Временной интервал'


admin.site.register(Doctors, DoctorsAdmin)
admin.site.register(Orders, OrdersAdmin)

admin.site.site_title = 'Панель управления поликлиникой'
admin.site.site_header = 'Панель управления поликлиникой'
