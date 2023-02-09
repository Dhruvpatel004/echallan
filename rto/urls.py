from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index,name="index"),
    path('rtodashboard/', views.rtodashboard,name="rtodashboard"),
    path('rlog/', views.log_rto,name="addp"),
    path('rtodashboard/rto_add_police/addp/', views.addp,name="saveinfopolice"),
    path('rtodashboard/rto_add_police/', views.addpo,name="addpolicepage"),
    path('rtodashboard/view_police_list/', views.allp,name="policelist"),
    path('rtodashboard/view_police_list/delete_pid/<int:pid>', views.delete_pid,name="dpolice"),
    path('rtodashboard/view_police_list/update_pid/<int:pid>', views.update_pid,name="upolice"),
    path('rtodashboard/view_police_list/update_pid/update_pid_record/<int:pid>', views.update_pid_record,name="updateifo"),
]
