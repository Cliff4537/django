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

def machine_list_view(request) :
  machines = Machine.objects.all()
  context = {'machines':  machines}
  return render(request, 'computerApp/machine_list.html',context)

def personnel_list_view(request) :
  Personnels= Personnel.objects.all()
  context = {'personnels': Personnels}
  return render(request, 'computerApp/personnel_list.html', context)


def machine_detail_view(request, pk ):
  machine = get_object_or_404( Machine , id = pk)
  context = { 'machine': machine}
  return render(request, 'computerApp/machine_detail.html', context)

def personnel_detail_view(request, pk ):
  personnel = get_object_or_404( Personnel , id = pk)
  context = { 'personnel': personnel}
  return render(request, 'computerApp/personnel_detail.html', context)

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
                administrateur=form.cleaned_data['administrateur']
                )
            new_machine.save()
            return redirect('machines')
    else:
        form = AddMachineForm()
    context = {'form': form}
    return render(request, 'computerApp/machine_add.html', context)

def infrastructure_add_form(request):
    if request.method == 'POST':
        form = AddInfrastructureForm(request.POST or None)
        if form.is_valid():
            new_infrastructure = Infrastructure(
                nom=form.cleaned_data['nom'],
                site=form.cleaned_data['site'],
                administrateur=form.cleaned_data['administrateur'],
                machines=form.cleaned_data['machines']
                )
            new_infrastructure.save()
            return redirect('infrastructures')
    else:
        form = AddInfrastructureForm()
    context = {'form': form}
    return render(request, 'computerApp/infra_add.html', context)




def infrastructure_list_view(request):
    infrastructure = Infrastructure.objects.all()
    context = {'infrastructure': infrastructure}
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
    form = AddPersonnelForm(request.POST or None)
    if form.is_valid():
      new_personnel = Personnel(
      nom=form.cleaned_data['nom'],
      genre=form.cleaned_data['genre'],
      prenom=form.cleaned_data['prenom'],
      site=form.cleaned_data['site'],
      machine = form.cleaned_data['machine'],
      role = form.cleaned_data['role'],
      email = form.cleaned_data['email'],
      telephone = form.cleaned_data['telephone']
      )
      new_personnel.save()
      return redirect ('personnels')
  else:
    form = AddPersonnelForm()
    context = {'form' : form}
    return render(request, 'computerApp/personnel_add.html',context)

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