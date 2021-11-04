from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns= [
    path("fetch",views.details,name="customerDetails"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("signup",views.signup,name="signup"),
    path("shownearest",views.shownearest,name="shownearest"),
    path("activeTrip",views.activetripforcustomer,name="activetripforcustomer")
]