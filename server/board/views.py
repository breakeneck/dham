from django.shortcuts import render, redirect
from .models import Node, Action, Scenario
import requests
from django.http import HttpResponse, JsonResponse


def nodes(request):
    nodes = Node.objects.prefetch_related('actions').filter(is_active__exact=1)
    return render(request, 'nodes.html', {'nodes': nodes})


def scenarios(request):
    scenarios = Scenario.objects.all().filter(is_running=0)
    return render(request, 'scenarios.html', {'scenarios': scenarios})


def scheduler(request):
    scenarios = Scenario.objects.all().filter(is_running=1)
    return render(request, 'scheduler.html', {'scenarios': scenarios})


# def run(request):
#     r = requests.get(request.GET('host') + request.GET('route'))
#     return HttpResponse(r.json())

# def run(request, host, route):
#     r = requests.get(host + '/' + route)
#     return HttpResponse(r.json())

# def run(request):
#     r = requests.get('http://192.168.88.102/measure')
#     return HttpResponse(r.content)


def run(request, node_id, action_id):
    node = Node.objects.get(pk=node_id)
    action = Action.objects.get(pk=action_id)
    r = requests.get('http://' + node.ip + '/' + action.route)
    return HttpResponse(r.content)


def schedule(request, scenario_id):
    scenario = Scenario.objects.get(pk=scenario_id)
    scenario.run()
    return redirect(scenarios)


def unschedule(request, scenario_id):
    scenario = Scenario.objects.get(pk=scenario_id)
    scenario.is_running = 0
    scenario.save()
    return redirect(scheduler)

