from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Destination, PackingList, PackingItem, TravelPlan, Photo
from .forms import TravelPlanForm, DestinationForm, PackingListForm


def index(request):
    travel_plans = TravelPlan.objects.all()
    return render(request, 'travelplanner/index.html', {'travel_plans': travel_plans})


def travel_plan_detail(request, travel_plan_id):
    travel_plan = get_object_or_404(TravelPlan, pk=travel_plan_id)
    return render(request, 'travelplanner/travel_plan_detail.html', {'travel_plan': travel_plan})


@login_required
def add_travel_plan(request):
    if request.method == 'POST':
        form = TravelPlanForm(request.POST)
        if form.is_valid():
            travel_plan = form.save(commit=False)
            travel_plan.user = request.user
            travel_plan.save()
            return redirect('travelplanner:travel_plan_detail', travel_plan_id=travel_plan.pk)
    else:
        form = TravelPlanForm()
    return render(request, 'travelplanner/add_travel_plan.html', {'form': form})


@login_required
def add_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.save()
            return redirect('travelplanner:destination_detail', destination_id=destination.pk)
    else:
        form = DestinationForm()
    return render(request, 'travelplanner/add_destination.html', {'form': form})


@login_required
def add_packing_list(request, travel_plan_id):
    travel_plan = get_object_or_404(TravelPlan, pk=travel_plan_id)
    if request.method == 'POST':
        form = PackingListForm(request.POST)
        if form.is_valid():
            packing_list = form.save(commit=False)
            packing_list.travel_plan = travel_plan
            packing_list.save()
            return redirect('travelplanner:packing_list_detail', travel_plan_id=travel_plan.pk,
                            packing_list_id=packing_list.pk)
    else:
        form = PackingListForm()
    return render(request, 'travelplanner/add_packing_list.html', {'form': form, 'travel_plan': travel_plan})


@login_required
def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, pk=destination_id)
    return render(request, 'travelplanner/destination_detail.html', {'destination': destination})


@login_required
def packing_list_detail(request, travel_plan_id, packing_list_id):
    travel_plan = get_object_or_404(TravelPlan, pk=travel_plan_id)
    packing_list = get_object_or_404(PackingList, pk=packing_list_id)
    packing_items = PackingItem.objects.filter(packing_list=packing_list)
    return render(request, 'travelplanner/packing_list_detail.html',
                  {'travel_plan': travel_plan, 'packing_list': packing_list, 'packing_items': packing_items})


@login_required
def add_packing_item(request, travel_plan_id, packing_list_id):
    travel_plan = get_object_or_404(TravelPlan, pk=travel_plan_id)

