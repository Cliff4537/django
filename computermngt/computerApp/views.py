from django.shortcuts import render, redirect
from computerApp.models import Machine,Personnel
from django.shortcuts import get_object_or_404
from .forms import AddMachineForm, AddPersonnelForm



def index(request) :
    machines = Machine.objects.all()
    Personnels = Personnel.objects.all()
    context = {
        'machines' : machines,
        'personnels': Personnels

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
  personnel = get_object_or_404( Personnel , secu = pk)
  context = { 'personnel': personnel}
  return render(request, 'computerApp/personnel_detail.html', context)

def machine_add_form(request):
    if request.method == 'POST':
        form = AddMachineForm(request.POST or None)
        if form.is_valid():
            new_machine = Machine(
                nom=form.cleaned_data['nom'],
                mach=form.cleaned_data['mach'])
            new_machine.save()
            return redirect('machines')
    else:
        form = AddMachineForm()
    context = {'form': form}
    return render(request, 'computerApp/machine_add.html', context)

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
      new_personnel = Personnel(nom=form.cleaned_data['nom'],
                        secu=form.cleaned_data['secu'])
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
