from django.urls import path

from . import views

urlpatterns = [
    path('', views.nodes, name='nodes'),
    # path(r'^run/(?P<host>)/(?P<route>)', views.run),
    # path('run/', views.run),
    # path(r'^run(.*)', views.run),
    # path('run/<slug:host>/<slug:route>', views.run),
    # path('run/', views.run),
    path('run/<int:node_id>/<int:action_id>', views.run),
    path('schedule/<int:scenario_id>', views.schedule),
    path('unschedule/<int:scenario_id>', views.unschedule),
    # path(r'^run/(<host>\w+)/(<route>\w+)$', views.run),
    path('scenarios/', views.scenarios),
    path('scheduler/', views.scheduler),
]