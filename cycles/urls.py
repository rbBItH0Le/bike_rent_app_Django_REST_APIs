from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns= [
    path("details",views.details,name="details"),
    path("track",views.track,name="track"),
    path("repair",views.repair,name="repair"),
    path("move",views.move,name="move")
]