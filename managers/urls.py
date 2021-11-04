from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns= [
    path("reports",views.reports,name="inde"),
    path("signup",views.signup,name="signup"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("addoperator",views.operatoronboard,name="operatoronboard"),
    path("showpie",views.showpie,name="showpie"),
    path("showstatbar",views.showstatbar,name="showstatbar"),
    path("showline",views.showline,name="showline"),
    path("showdetail",views.showdetail,name="showdetail"),
    path("starttripgraph",views.starttripgraph,name="starttripgraph"),
    path("endtripgraph",views.endtripgraph,name="endtripgraph"),
    path("availdamagbar",views.availdamagbar,name="availdamagbar"),
]