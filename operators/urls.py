from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns= [
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("details",views.details,name="details"),
    path("addstation",views.addstation,name="addstation"),
    path("showstation",views.showstation,name="showstation"),
    path("addcycles",views.addcycles,name="addcycles"),
    path("deletecycle",views.deletecycle,name="deletecycle"),
    path("movecycle",views.movecycle,name="movecycle"),
    path("showcycle",views.showcycle,name="showcycle")
]