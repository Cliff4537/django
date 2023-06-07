from django.shortcuts import render, redirect
from computerApp.models import Machine,Personnel,Infrastructure,MachineUpdate
from django.shortcuts import get_object_or_404
from .forms import AddMachineForm, AddPersonnelForm, AddInfrastructureForm
import urllib.request
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.urls import reverse
from datetime import timedelta
from django.utils import timezone




def index(request) :
    machines = Machine.objects.all()
    Personnels = Personnel.objects.all()
    infrastructures = Infrastructure.objects.all()
    context = {
        'machines' : machines,
        'personnels': Personnels,
        'infrastructures' : infrastructures

    }
    return render(request, 'index.html',context)
@login_required
def machine_list_view(request):
    search_query = request.GET.get('search_query')
    filter_type = request.GET.get('filter_type')
    filter_date = request.GET.get('filter_date')
    filter_site = request.GET.get('filter_site')
    

    machines = Machine.objects.all()


    if search_query:
        machines = machines.filter(nom__icontains=search_query)

    if filter_type:
        machines = machines.filter(mach=filter_type)

    if filter_date == 'recent':
        machines = machines.order_by('-creation_date')
    elif filter_date == 'ancient':
        machines = machines.order_by('creation_date')

    if filter_site:
        machines = machines.filter(site=filter_site)

    context = {
        'machines': machines,
        'search_query': search_query,
        'filter_type': filter_type,
        'filter_date': filter_date,
        'filter_site': filter_site
    }
    return render(request, 'computerApp/machine_list.html', context)

  
@login_required
def update_machine(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)

    if request.method == 'POST':
        
        return redirect('machine-list')
    return render(request, 'update_machine.html', {'machine': machine})

@login_required
def personnel_list_view(request):
    personnels = Personnel.objects.all()

    # Filtrage par genre
    filter_genre = request.GET.get('filter_genre')
    if filter_genre:
        personnels = personnels.filter(genre=filter_genre)

    # Filtrage par site
    filter_site = request.GET.get('filter_site')
    if filter_site:
        personnels = personnels.filter(site=filter_site)

    # Filtrage par rôle
    filter_role = request.GET.get('filter_role')
    if filter_role:
        personnels = personnels.filter(role=filter_role)

    # Recherche
    search_query = request.GET.get('search_query')
    if search_query:
        personnels = personnels.filter(nom__icontains=search_query) | personnels.filter(prenom__icontains=search_query)

    context = {'personnels': personnels, 'search_query': search_query, 'filter_genre': filter_genre, 'filter_site': filter_site, 'filter_role': filter_role}
    return render(request, 'computerApp/personnel_list.html', context)

@login_required   
def update_machine(request, pk):
    machine = get_object_or_404(Machine, pk=pk)
    
    # Récupérer le type de machine
    machine_type = machine.mach
    
    # Définir le delta de maintenance en fonction du type de machine
    if machine_type == 'PC':
        maintenance_delta = timedelta(days=7)
    elif machine_type == 'Mac':
        maintenance_delta = timedelta(days=7)
    elif machine_type == 'Serveur':
        maintenance_delta = timedelta(days=14)
    elif machine_type == 'Switch':
        maintenance_delta = timedelta(days=28)
    else:
        maintenance_delta = timedelta(days=0)
    
    # Calculer la nouvelle date de maintenance
    current_date = timezone.now()
    new_maintenance_date = current_date + maintenance_delta
    
    # Mettre à jour la date de maintenance seulement si elle a changé
    if machine.maintenance_date != new_maintenance_date:
        machine.maintenance_date = new_maintenance_date
        machine.save(update_fields=['maintenance_date'])

    MachineUpdate.objects.create(machine=machine, admin=request.user)
    
    # Rediriger vers la page "machines" avec les machines mises à jour
    return redirect('machines')
@login_required
def machine_detail_view(request, pk ):
  machine = get_object_or_404( Machine , id = pk)
  context = { 'machine': machine}
  return render(request, 'computerApp/machine_detail.html', context)

@login_required 
def delete_machine(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)

    if request.method == 'POST':
        machine.delete()
        return redirect('machines')

    return render(request, 'computerApp/delete_machine.html', {'machine': machine})
@login_required
def delete_personnel(request, personnel_id):
    personnel = get_object_or_404(Personnel, id=personnel_id)

    if request.method == 'POST':
        personnel.delete()
        return redirect('personnels')

    return render(request, 'computerApp/delete_personnel.html', context = {'personnel': personnel})

@login_required
def delete_infrastructure(request, infrastructure_id):
    infrastructure = get_object_or_404(Infrastructure, id=infrastructure_id)

    if request.method == 'POST':
        infrastructure.delete()
        return redirect('infrastructures')

    return render(request, 'computerApp/delete_infrastructure.html', context = {'infrastructure': infrastructure})    
    

@login_required
def personnel_detail_view(request, pk ):
  personnel = get_object_or_404( Personnel , id = pk)
  context = { 'personnel': personnel}
  return render(request, 'computerApp/personnel_detail.html', context)

@login_required
def infrastructure_detail_view(request, pk):
    infrastructure = get_object_or_404(Infrastructure, id = pk)
    machines = infrastructure.machines.all()  
    context = {
        'infrastructure': infrastructure,
        'machines': machines,
    }
    return render(request, 'computerApp/infra_detail.html', context)

@login_required
def machine_add_form(request):
    if request.method == 'POST':
        form = AddMachineForm(request.POST or None)
        if form.is_valid():
            new_machine = Machine(
                nom=form.cleaned_data['nom'],
                mach=form.cleaned_data['mach'],
                address_ip=form.cleaned_data['address_ip'],
                personnel=form.cleaned_data['personnel'],
                site=form.cleaned_data['site'],
                administrateur=form.cleaned_data['administrateur'],
                creation_date=form.cleaned_data['creation_date']
                )
            new_machine.save()
            return redirect('machines')
    else:
        form = AddMachineForm()
    context = {'form': form}
    return render(request, 'computerApp/machine_add.html', context)


@login_required
def infrastructure_add_form(request):
    if request.method == 'POST':
        form = AddInfrastructureForm(request.POST)
        if form.is_valid():
            # Traitement des données valides
            nom = form.cleaned_data['nom']
            site = form.cleaned_data['site']
            machines = form.cleaned_data['machines']
            administrateur = form.cleaned_data['administrateur']

            new_infrastructure = Infrastructure(
                nom=nom,
                site=site,
                administrateur=administrateur
            )
            new_infrastructure.save()

            # Ajouter les machines sélectionnées à l'infrastructure
            new_infrastructure.machines.set(machines)

            return redirect('infrastructures')
    else:
        form = AddInfrastructureForm()
    context = {'form': form}
    return render(request, 'computerApp/infra_add.html', context)





@login_required
def infrastructure_list_view(request):
    infrastructures = Infrastructure.objects.all()
    context = {'infrastructures': infrastructures}
    return render(request, 'computerApp/infra_list.html', context)

@login_required
def personnel_add_form(request):
    if request.method == 'POST':
        form = AddPersonnelForm(request.POST)
        if form.is_valid():
            # Traitement des données valides
            new_personnel = Personnel(
                nom=form.cleaned_data['nom'],
                genre=form.cleaned_data['genre'],
                prenom=form.cleaned_data['prenom'],
                site=form.cleaned_data['site'],
                machine=form.cleaned_data['machine'],
                role=form.cleaned_data['role'],
                email=form.cleaned_data['email'],
                telephone=form.cleaned_data['telephone'],
            )
            new_personnel.save()
            return redirect('personnels')
    else:
        form = AddPersonnelForm()
    
    context = {'form': form}
    return render(request, 'computerApp/personnel_add.html', context)





@login_required
def weather_view(request):
    cities = ['Paris', 'Tours']
    api_url = 'https://api.api-ninjas.com/v1/weather?city={}'
    headers = {'X-Api-Key': 'vmXT4EVa9Venw5Kq7PXiRA==VJTSWcdc0SFRtOEg'}
    weather_data = []

    for city in cities:
        req = urllib.request.Request(api_url.format(city), headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())

                temperature = data['temp']
                wind_speed = data['wind_speed']
                wind_degrees = data['wind_degrees']
                humidity = data['humidity']
                sunset = data['sunset']
                min_temp = data['min_temp']
                cloud_pct = data['cloud_pct']
                feels_like = data['feels_like']
                sunrise = data['sunrise']
                max_temp = data['max_temp']

                city_weather = {
                    'city': city,
                    'temperature': int(temperature),
                    'wind_speed': float(wind_speed),
                    'wind_degrees': int(wind_degrees),
                    'humidity': int(humidity),
                    'sunset': int(sunset),
                    'min_temp': int(min_temp),
                    'cloud_pct': int(cloud_pct),
                    'feels_like': int(feels_like),
                    'sunrise': int(sunrise),
                    'max_temp': int(max_temp)
                }
                weather_data.append(city_weather)

        except urllib.error.HTTPError as e:
            error_message = "Error: {} - {}".format(e.code, e.reason)
            return render(request, 'computerApp/weather.html', {'error_message': error_message})

    context = {'weather_data': weather_data}
    return render(request, 'computerApp/weather.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirige vers la page d'accueil après la connexion
        else:
            error_message = 'Identifiant ou mot de passe incorrect'
            return render(request, 'computerApp/login.html', {'error_message': error_message})
    else:
        return render(request, 'computerApp/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
@login_required       
def dashboard_view(request):
    # Récupérer les dernières mises à jour des machines
    machine_updates = MachineUpdate.objects.all().order_by('-update_date')
    
    return render(request, 'computerApp/dashboard.html', {'machine_updates': machine_updates})

def home_view(request):
    return render(request, 'home.html')

