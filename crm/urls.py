from django.urls import path
from .views import doctor_approval, date_approval, time_approval, final_approval
urlpatterns = [
    path('', doctor_approval, name='doctor_approval'),
    path('<int:doctor>/', date_approval, name='date_approval'),
    path('<int:doctor>/<int:ord_date>/', time_approval, name='time_approval'),
    path('<int:doctor>/<int:ord_date>/<int:period>/', final_approval, name='final_approval'),
]
