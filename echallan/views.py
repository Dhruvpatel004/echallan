
# Create your views here.
from datetime import *
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from police.models import Police
from rto.models import Challan, Rules, Vehicle 
from django.contrib import messages
# Create your views here.
def index(request):

    return render(request,'index.html')

def user(request):
    v_no=request.GET.get('vehicleNumber','GJ00XX0000')
    
    vexist = Vehicle.objects.filter(vehicle_no=v_no).count()

    # ab=request.GET.get("text1",'default')
    print(vexist)
    if vexist:
        c=list(Challan.objects.all().filter(vehicle_no=v_no))
        pen=Challan.objects.filter(status='Pending',vehicle_no=v_no).count()
        p=Challan.objects.filter(status='Paid',vehicle_no=v_no).count()
        return render(request,"user.html",{'v':v_no ,'c':c,'pen':pen,'p':p})
    else:
        return redirect ('../')
    
def  paid(request,cno):
    c=Challan.objects.get(challan_no=cno)
    v=c.vehicle_no
    c.status='Paid'
    c.save()
    return redirect('../?vehicleNumber='+v) 

def challan(request,cno):
    
        c=Challan.objects.get(challan_no=cno)
        r_code=c.rule_code
        r=Rules.objects.get(rule_code=r_code)
        v_no=c.vehicle_no
        v=Vehicle.objects.get(vehicle_no=v_no)
        context = {
            'user': user(request),
            'c':c,
            'r':r,
            'v':v
        }
        return render(request, 'challan.html', context)

def invoice(request,cno):
    
        c=Challan.objects.get(challan_no=cno)
        r_code=c.rule_code
        r=Rules.objects.get(rule_code=r_code)
        v_no=c.vehicle_no
        v=Vehicle.objects.get(vehicle_no=v_no)
        context = {
            'user': user(request),
            'c':c,
            'r':r,
            'v':v
        }
        return render(request, 'r.html', context)
   

