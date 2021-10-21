from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns= [
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("details",views.details,name="details"),
    path("return",views.returns,name="return"),
    path("report",views.report,name="report"),
    path("pay",views.pay,name="pay"),
    
]