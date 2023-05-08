from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('machines/',views.machine_list_view, name='machines'),
    path('personnels/',views.personnel_list_view, name='personnels' ),
    path('machines/<pk>',views.machine_detail_view, name = 'machine-detail'), 
    path('personnels/<pk>',views.personnel_detail_view, name = 'personnel-detail'), 
    path('add-machine', views.machine_add_form, name = 'add-machine'),
    path('add-personnel', views.personnel_add_form, name = 'add-personnel')
]