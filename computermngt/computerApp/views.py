from django.shortcuts import render, redirect
from computerApp.models import Machine,Personnel,Infrastructure
from django.shortcuts import get_object_or_404
from .forms import AddMachineForm, AddPersonnelForm, AddInfrastructureForm



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

  

def personnel_list_view(request) :
  Personnels= Personnel.objects.all()
  context = {'personnels': Personnels}
  return render(request, 'computerApp/personnel_list.html', context)



def machine_detail_view(request, pk ):
  machine = get_object_or_404( Machine , id = pk)
  context = { 'machine': machine}
  return render(request, 'computerApp/machine_detail.html', context)
  
def delete_machine(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)

    if request.method == 'POST':
        machine.delete()
        return redirect('machines')

    return render(request, 'computerApp/delete_machine.html', {'machine': machine})


def personnel_detail_view(request, pk ):
  personnel = get_object_or_404( Personnel , id = pk)
  context = { 'personnel': personnel}
  return render(request, 'computerApp/personnel_detail.html', context)

def infrastructure_detail_view(request, pk ):
  infrastructure = get_object_or_404( Infrastructure , id = pk)
  context = { 'infrastructure': infrastructure}
  return render(request, 'computerApp/infra_detail.html', context)

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

# def get_admin(request):
#     if request.method == 'POST':
#         personnels = Personnel.objects.filter(role='Administrateur')
#         admins = []
#         for personnel in personnels:
#             admins.append(personnel)
#     context = {'admins': admins}
#     return render(request, 'computerApp/machine_add.html', context)

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

# def infrastructure_add_form(request):
#     if request.method == 'POST':
#         form = AddInfrastructureForm(request.POST)
#         if form.is_valid():
#             new_infrastructure = form.save()
#             return redirect('infrastructures')
#     else:
#         form = AddInfrastructureForm()
#     context = {'form': form}
#     return render(request, 'computerApp/infra_add.html', context)




def infrastructure_list_view(request):
    infrastructures = Infrastructure.objects.all()
    context = {'infrastructures': infrastructures}
    return render(request, 'computerApp/infra_list.html', context)
# def machine_add_form(request):
#   if request.method == 'POST':
#     form = AddMachineForm(request.POST or None)
#     if form.is_valid():
#       new_machine = Machine(nom=form.cleaned_data['nom'])
#       # TYPE=form.cleaned_data['TYPE'])
#       new_machine.save()
#       return redirect ('machines')
#   else:
#     form = AddMachineForm()
#     context = {'form' : form}
#     return render(request, 'computerApp/machine_add.html',context)

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

# Create your views here.
# Ajout de la ligne de recuperation des machine
# m a c h i n e s = M a c h i n e . o b j e c t s . a l l ( )
# il existe d’autres moyens de filtrer
# au moment de recuperer les donnees
## Filtrage par numero de machine
### machines = Machine.objects.filter(id=1)
## Filtrage par debut de nom
### machines = Machine.objects.filter(nom_startwith=’10’)
## Trier les machines selon un champ particulier
### machines = Machine.objects.order_by(’−id’)