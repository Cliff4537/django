from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home_view, name='home'),
    path('index/', views.index, name='index'),
    path('machines/',views.machine_list_view, name='machines'),
    path('personnels/',views.personnel_list_view, name='personnels' ),
    path('machines/<pk>',views.machine_detail_view, name = 'machine-detail'), 
    path('personnels/<pk>',views.personnel_detail_view, name = 'personnel-detail'), 
    path('infrastructures/<pk>',views.infrastructure_detail_view, name = 'infrastructure-detail'),
    path('add-machine', views.machine_add_form, name = 'add-machine'),
    path('add-personnel', views.personnel_add_form, name = 'add-personnel'),
    path('infrastructures/',views.infrastructure_list_view, name='infrastructures'),
    path('add_infrastructure/', views.infrastructure_add_form, name='add-infra'),
    path('machines/delete/<int:machine_id>/', views.delete_machine, name='delete_machine'),
    path('personnels/delete/<int:personnel_id>/', views.delete_personnel, name='delete_personnel'),
    path('infrastructures/delete/<int:infrastructure_id>/',views.delete_infrastructure, name='delete_infrastructure'),
    path('machine/update/<int:pk>/', views.update_machine, name='update_machine'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('Meteo/',views.weather_view, name='meteo'),
    path('maj/',views.update_machine, name='maj' ),
    path('dashboard/', views.dashboard_view, name='dashboard')

]