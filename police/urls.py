from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # path('',views.i),
    # path('admin/', admin.site.urls),
path('', views.index2,name="index2"),
    path('policedashboard/', views.policedashboard,name="policedashboard"),
    path('plog/', views.log_police,name="addp"),

    # path('login/', views.handleLogin, name='handleLogin'),
    # path('logout/', views.handleLogout, name='handleLogout'),
    path('policedashboard/generate_challan/addc/', views.addc,name="savegeneratechallanpage"),
    path('policedashboard/generate_challan/', views.addce,name="generatechallanpage"),
    path('policedashboard/history/pending/', views.allcpending,name="pendinglist"),
    path('policedashboard/history/pending/pchallan/<int:cno>', views.pchallan,name="pendinglist"),
    path('policedashboard/history/paid/', views.allcpaid,name="paidlist"),
    path('policedashboard/history/paid/pchallan/<int:cno>', views.pchallan,name="paidlist"),
    path('policedashboard/profile/', views.profile, name="police_Profile"),
    path('policedashboard/profile/changepassword/', views.changepassword, name="police_Profile"),
    path('policedashboard/pchallan/<int:cno>', views.pchallan,name="pendinglist"),
    # path('policedashboard/generate_challan/<str:vid>', views.profile,name="uv"),


    # path('policedashboard/generate_challan/', views.addce,name="generatechallanpage"),

    
    path('policedashboard/generate_challan/validate-vehical-number', csrf_exempt(views.validate_vehical_number_api),name="vnoapi"),
    path('policedashboard/generate_challan/<str:vid>', views.show_vid,name="uv"),



]
