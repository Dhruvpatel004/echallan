from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index2,name="index2"),
    path('policedashboard/', views.policedashboard,name="policedashboard"),
    # path('login/', views.handleLogin, name='handleLogin'),
    # path('logout/', views.handleLogout, name='handleLogout'),


]
