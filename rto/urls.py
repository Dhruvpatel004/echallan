from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


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
    path('rtodashboard/view_police_list/show_pid/<int:pid>', views.show_pid,name="upolice"),
    path('rtodashboard/view_police_list/update_pid/update_pid_record/<int:pid>', views.update_pid_record,name="updateifo"),

    path('rtodashboard/rto_add_vehicle/', views.addve, name="rto_add_vehicle"),
    path('rtodashboard/rto_add_vehicle/addv/', views.addv,name="saveinfovehicle"),
    path('rtodashboard/view_vehicle_list/', views.allv,name="vehiclelist"),
    path('rtodashboard/view_vehicle_list/update_vid/<int:vid>', views.update_vid,name="uve"),
    path('rtodashboard/view_vehicle_list/update_vid/update_vid_record/<int:vid>', views.update_vid_record,name="updateifo"),
    path('rtodashboard/view_vehicle_list/delete_vid/<int:vid>', views.delete_vid,name="dv"),
    path('rtodashboard/view_vehicle_list/show_vid/<int:vid>', views.show_vid,name="uv"),

    path('rtodashboard/rto_add_rule/', views.addr, name="rto_add_rule"),
    path('rtodashboard/rto_add_rule/addrl/', views.addrl,name="saveinforule"),
    path('rtodashboard/view_rule_list/', views.allrule,name="vehiclelist"),
    path('rtodashboard/view_rule_list/update_rid/<int:rid>', views.update_rid,name="uve"),
    path('rtodashboard/view_rule_list/update_rid/update_rid_record/<int:rid>', views.update_rid_record,name="updateifo"),
    path('rtodashboard/view_rule_list/delete_rid/<int:rid>', views.delete_rid,name="dr"),
    path('rtodashboard/view_rule_list/show_rid/<int:rid>', views.show_rid,name="ur"),

    path('rtodashboard/profile/', views.profile, name="rto_Profile"),
    path('rtodashboard/profile/changepassword/', views.changepassword, name="rto_Profile"),
    path('rtodashboard/upcomig/', views.upcoming,name="saveinfopolice"),


    #api calls form client
    path('rtodashboard/rto_add_police/validate-username', csrf_exempt(views.validate_username_api),name="api"),
    path('rtodashboard/rto_add_vehicle/validate-vehical-number', csrf_exempt(views.validate_vehical_number_api),name="vnoapi"),
    path('rtodashboard/rto_add_vehicle/validate-vehical-engine-number', csrf_exempt(views.validate_vehical_engine_number_api),name="venoapi"),
    path('rtodashboard/rto_add_vehicle/validate-vehical-chassics-number', csrf_exempt(views.validate_vehical_chassics_number_api),name="vcnoapi"),
    path('rtodashboard/rto_add_rule/validate-rule-code', csrf_exempt(views.validate_rule_code_api),name="vcnoapi"),
    path('rtodashboard/challan_history/', views.allcrto,name="challanlist"),

    # path('rtodashboard/challan_history/rchallan/', views.allcpending,name="list"),
    path('rtodashboard/challan_history/rchallan/<int:cno>', views.rchallan,name="list"),

]
