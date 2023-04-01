from datetime import *
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib import messages
from .models import Police
# Create your views here.
from datetime import *
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import Police
from rto.models import Challan, Rules, Vehicle 
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
import json
from django.http import JsonResponse
# Create your views here.
def i(request):
    return render(request,'tree.html')

def authcheck(request):
    if request.session.get('login') == False or request.session.get('username') == None:
            # messages.success(request, 'Login needed')
            return False
    else :
        return True
# Create your views here.

def user(request):
    
    user_info={
        'username':request.session.get('username')
    }

    return user_info

def index2(request):
    request.session['login'] = False
    request.session['username'] = None
    return render(request,'police.html')


def user(request):
    
    user_info={
        'username':request.session.get('username')
    }

    return user_info



def policedashboard(request):
    if request.method == 'POST':

        username = request.POST.get('policeemail', 'default')
        password = request.POST.get('policepassword', 'default')
 
        cusername = Police.objects.filter(
        police_username=username, police_password=password).count()
        request.session['loginid'] = username
        extra=datetime.now().date()
        if extra.month-1 == 2 and extra.day>28:
            monthbefore=date(extra.year,(extra.month-1),28)
        elif extra.day == 31 :
            monthbefore=date(extra.year,(extra.month-1),30)
        else:
            monthbefore=date(extra.year,(extra.month-1),extra.day)

        if extra.month-2 == 2 and extra.day>28:
            monthbeforebefore=date(extra.year,(extra.month-2),28) 
        elif extra.day == 31 :
            monthbeforebefore=date(extra.year,(extra.month-2),30)
        else:
            monthbeforebefore=date(extra.year,(extra.month-2),extra.day)
        yesterday=datetime.now().date()-timedelta(1)
        # monthbefore=monthbefore.month-1
        tallchs = list(Challan.objects.filter(offence_date=datetime.now().date()).filter(cpolice=username).values())
        yallchs = list(Challan.objects.filter(offence_date=yesterday).filter(cpolice=username).values())

        sumallchs = list(Challan.objects.filter(offence_date=datetime.now().date()).filter(cpolice=username))
        yesterdaysumallchs = list(Challan.objects.filter(offence_date=yesterday).filter(cpolice=username))

        nowtotalchs = list(Challan.objects.filter(offence_date__gte=monthbefore,offence_date__lte=datetime.now().date()).filter(cpolice=username))
        lasttotalchs = list(Challan.objects.filter(offence_date__gte=monthbeforebefore,offence_date__lte=monthbefore).filter(cpolice=username))

        paidtotalchs = list(Challan.objects.filter(offence_date__gte=monthbefore,offence_date__lte=datetime.now().date()).filter(status="Paid").filter(cpolice=username))
        pendingtotalchs = list(Challan.objects.filter(offence_date__gte=monthbefore,offence_date__lte=datetime.now().date()).filter(status="Pending").filter(cpolice=username))

        
        total_sum_today = 0
        for item in sumallchs:
            total_sum_today += item.fine

        total_sum_yesterday = 0
        for item in yesterdaysumallchs:
            total_sum_yesterday += item.fine
        if total_sum_today + total_sum_yesterday==0:
            challan_difference_today=0
            challan_difference_yesterday=0
        else:
            challan_difference_today= ((total_sum_today*100)/(total_sum_today + total_sum_yesterday))
            challan_difference_yesterday=(total_sum_yesterday*100)/(total_sum_today+total_sum_yesterday)

        total_sum_month = 0
        for item in nowtotalchs:
            total_sum_month += item.fine

        last_total_sum_month = 0
        for item in lasttotalchs:
            last_total_sum_month += item.fine

        if total_sum_month + last_total_sum_month==0:
            challan_difference_lmonth=0
            challan_difference_tmonth=0
        else:
            challan_difference_tmonth= ((total_sum_month*100)/(total_sum_month + last_total_sum_month))
            challan_difference_lmonth=(last_total_sum_month*100)/(total_sum_month+last_total_sum_month)

        paid_total_sum_month = 0
        for item in paidtotalchs:
            paid_total_sum_month += item.fine

        pending_total_sum_month = 0
        for item in pendingtotalchs:
            pending_total_sum_month += item.fine

        c = request.session.get('username')
        v = request.session.get('username')
        if cusername:
            request.session['login'] = True
            request.session['username'] = username

            context = {
                'user': user(request),
                'c': tallchs ,
                'cl': len(tallchs),
                'ycl': len(yallchs),
                'cgtyc': round(len(tallchs)-len(yallchs)),
                'ycgtc': round(len(yallchs)-len(tallchs)), 
                'sumt' : total_sum_today,
                'summ' : total_sum_month,
                'paidsumm' : paid_total_sum_month,
                'pendingsumm' : pending_total_sum_month,
                'challandifftoday' : challan_difference_today,
                'challandiffyesterday': challan_difference_yesterday,
                'tgtchallandiffday' : round(challan_difference_today-challan_difference_yesterday),
                'ygtchallandiffday' : round(challan_difference_yesterday-challan_difference_today),
                'challandiffthismonth' : challan_difference_tmonth,
                'challandifflastmonth': challan_difference_lmonth,
                'ngtchallandiffmonth' : round(challan_difference_tmonth-challan_difference_lmonth),
                'lgtchallandiffmonth' : round(challan_difference_lmonth-challan_difference_tmonth)
                          }




        # allchs = list(Vehicle.objects.all().values())
        # print(allpoli




            return render(request, 'policedashboard.html', context)

        else:
            messages.warning(request, 'Invalid Credentials')
            return redirect('../')

    else:
        if request.session.get('login') == False or request.session.get('username') == None:
            # messages.success(request, 'Login needed')
            return redirect('/police/')

        else:
            a=user(request)
            username = request.POST.get('policeemail',a['username'])
            password = request.POST.get('policepassword', a['username'])
            print(username,'-----------')
 
            cusername = Police.objects.filter(
            police_username=username, police_password=password).count()
            request.session['loginid'] = username
        # print(cusername)
            extra=datetime.now().date()
            if extra.month-1 == 2 and extra.day>28:
                monthbefore=date(extra.year,(extra.month-1),28)
            elif extra.day == 31 :
                monthbefore=date(extra.year,(extra.month-1),30)
            else:
                monthbefore=date(extra.year,(extra.month-1),extra.day)

            if extra.month-2 == 2 and extra.day>28:
                monthbeforebefore=date(extra.year,(extra.month-2),28) 
            elif extra.day == 31 :
                monthbeforebefore=date(extra.year,(extra.month-2),30)
            else:
                monthbeforebefore=date(extra.year,(extra.month-2),extra.day)
            yesterday=datetime.now().date()-timedelta(1)
        # monthbefore=monthbefore.month-1
            tallchs = list(Challan.objects.filter(offence_date=datetime.now().date()).filter(cpolice=username).values())
            yallchs = list(Challan.objects.filter(offence_date=yesterday).filter(cpolice=username).values())

            sumallchs = list(Challan.objects.filter(offence_date=datetime.now().date()).filter(cpolice=username))
            yesterdaysumallchs = list(Challan.objects.filter(offence_date=yesterday).filter(cpolice=username))

            nowtotalchs = list(Challan.objects.filter(offence_date__gte=monthbefore,offence_date__lte=datetime.now().date()).filter(cpolice=username))
            lasttotalchs = list(Challan.objects.filter(offence_date__gte=monthbeforebefore,offence_date__lte=monthbefore).filter(cpolice=username))

            paidtotalchs = list(Challan.objects.filter(offence_date__gte=monthbefore,offence_date__lte=datetime.now().date()).filter(status="Paid").filter(cpolice=username))
            pendingtotalchs = list(Challan.objects.filter(offence_date__gte=monthbefore,offence_date__lte=datetime.now().date()).filter(status="Pending").filter(cpolice=username))

        
            total_sum_today = 0
            for item in sumallchs:
                total_sum_today += item.fine

            total_sum_yesterday = 0
            for item in yesterdaysumallchs:
                total_sum_yesterday += item.fine
            if total_sum_today + total_sum_yesterday==0:
                challan_difference_today=0
                challan_difference_yesterday=0
            else:
                challan_difference_today= ((total_sum_today*100)/(total_sum_today + total_sum_yesterday))
                challan_difference_yesterday=(total_sum_yesterday*100)/(total_sum_today+total_sum_yesterday)

            total_sum_month = 0
            for item in nowtotalchs:
                total_sum_month += item.fine

            last_total_sum_month = 0
            for item in lasttotalchs:
                last_total_sum_month += item.fine

            if total_sum_month + last_total_sum_month==0:
                challan_difference_lmonth=0
                challan_difference_tmonth=0
            else:
                challan_difference_tmonth= ((total_sum_month*100)/(total_sum_month + last_total_sum_month))
                challan_difference_lmonth=(last_total_sum_month*100)/(total_sum_month+last_total_sum_month)

            paid_total_sum_month = 0
            for item in paidtotalchs:
                paid_total_sum_month += item.fine

            pending_total_sum_month = 0
            for item in pendingtotalchs:
                pending_total_sum_month += item.fine

            c = request.session.get('username')
            v = request.session.get('username')
            if cusername:
                request.session['login'] = True
                request.session['username'] = username

            context = {
                'user': user(request),
                'c': tallchs ,
                'cl': len(tallchs),
                'ycl': len(yallchs),
                'cgtyc': round(len(tallchs)-len(yallchs)),
                'ycgtc': round(len(yallchs)-len(tallchs)), 
                'sumt' : total_sum_today,
                'summ' : total_sum_month,
                'paidsumm' : paid_total_sum_month,
                'pendingsumm' : pending_total_sum_month,
                'challandifftoday' : challan_difference_today,
                'challandiffyesterday': challan_difference_yesterday,
                'tgtchallandiffday' : round(challan_difference_today-challan_difference_yesterday),
                'ygtchallandiffday' : round(challan_difference_yesterday-challan_difference_today),
                'challandiffthismonth' : challan_difference_tmonth,
                'challandifflastmonth': challan_difference_lmonth,
                'ngtchallandiffmonth' : round(challan_difference_tmonth-challan_difference_lmonth),
                'lgtchallandiffmonth' : round(challan_difference_lmonth-challan_difference_tmonth)
                          }
            
            return render(request, 'policedashboard.html', context)
def send_email(request,emaill,context):
    # email1=request.POST.get('user_email')
    # print(email1
    #       )
    template = render_to_string('email_tem.html',context)
    email =  EmailMultiAlternatives(
        'Testing Email of Echallan',
        template,
        settings.EMAIL_HOST_USER,
        # ['pateldhruvn2004@gmail.com','21cs041@charusat.edu.in'],
        [emaill],
    )
    email.attach_alternative(template, "text/html")
    email.fail_silently=False
    email.send()
        
def addc(request):
    if authcheck(request):
        c_police_id = request.session['username']
        if request.method == "POST":
            
            sus_name=request.POST.get('sus_name')
            # l_no = request.POST.get('li_no')
            v_no = request.POST.get('v_no')
            # o_mobile_no = request.POST.get('v_own_conno')
            rule_c = request.POST.get('section')
            evi = request.POST.get('evid')
            print(rule_c)
            vehicle=Vehicle.objects.get(vehicle_no=v_no)
            rule = Rules.objects.get(rule_code=rule_c)

            Challans = Challan(cpolice=c_police_id , suspect_name=sus_name, offence_date=datetime.now().date(), offence_time=datetime.now().time(),offender_email_id=vehicle.vehicle_own_email ,
                        owner_name=vehicle.vehicle_own_name,vehicle_no=v_no, offender_mobile_no=vehicle.vehicle_own_contact,
                        rule_code=rule.rule_code,evidence=evi,fine=rule.rule_pen)
            Challans.save()
            
            # v=Vehicle.objects.get(vehicle_no=v_no)
            c=Challan.objects.last()
            context = {
                # 'user': user(request),
                'v':vehicle,
                'c':c,
                'r':rule.rule_desc
            }
            send_email(request,vehicle.vehicle_own_email,context)
            messages.success(request,"Challan Generated Successfully of "+v_no)
            return redirect('../')

    else:
        return log_police(request)

def addce(request):
    if authcheck(request):
        allrules = list(Rules.objects.all().values())
        # allchs = list(Vehicle.objects.all().values())
        # print(allpoli)
        c = request.session.get('username')
        v = request.session.get('username')
 
        context1 = {
            'user': user(request),
            'r': allrules                  
            }
        
        return render(request, 'generate_challan.html',context1)
    else:
        return log_police(request)

def log_police(request):
    request.session['login'] = False
    request.session['username'] = None
    return redirect('/police/')


def allcpending(request):
    if authcheck(request):
        allchs = list(Challan.objects.filter(status='Pending').values().reverse())
        # allchs = list(Vehicle.objects.all().values())
        # print(allpoli)
        c = request.session.get('username')
        v = request.session.get('username')
 
        context1 = {
            'user': user(request),
            'c': allchs                    
            }
        return render(request, 'pending.html',context1)

    else:
        return log_police(request)
    
def allcpaid(request):
    if authcheck(request):
        allchs = list(Challan.objects.filter(status='Paid').reverse())

        c = request.session.get('username')
        v = request.session.get('username')

        context1 = {
            'user': user(request),
            'c': allchs                    
            }

        return render(request, 'paid.html',context1)

    else:
        return log_police(request)
    





def profile(request):

    if authcheck(request):
        u=request.session.get('username')
        p=Police.objects.get(police_username=u)
        context = {
            'user': user(request),
            'p':p
        }
        return render(request, 'police_profile.html', context)

    else:
        return log_police()

def changepassword(request):

    if authcheck(request):
        
        if request.method == "POST":
            cpassword = request.POST.get('password')
            npassword = request.POST.get('newpassword')
            renpassword= request.POST.get('renewpassword')
            username= request.POST.get('policeusername')

            print("C  : ",cpassword)
            print("n  : " ,npassword)
            print("RN : ",renpassword)
            if npassword != renpassword:
                messages.warning(request, 'New password does not match with re-enterd password')
            else:
                # rto = RTOadmin.objects.get(admin_username=username)
                p=Police.objects.get(police_username=username)

                print(p.police_password)
                print(cpassword)
                if p.police_password==cpassword:
                    p.police_password=npassword
                    p.save()
                    messages.success(request, 'Password is changed successfuly ')
                
                else:
                    messages.warning(request, 'Current password does not match.')
                    
        return redirect('../')
    else:
        return log_police()
    
#challan show 
def pchallan(request,cno):
    if authcheck(request):
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
        return render(request, 'pchallan.html', context)
    else:
        return log_police()
    
def show_vid(request, vid):

    if authcheck(request):
        vehicle = Vehicle.objects.get(vehicle_no=vid)
    
        context = {
            'user': user(request),
            'member':vehicle,
            'access':False

            }
        return render(request, 'view_v.html', context)
    
    else:
        return log_police()
    
#api
def validate_vehical_number_api(request):
    data = json.loads(request.body)
    vnum = data['vehical_number']

    vnumtaken = Vehicle.objects.filter(vehicle_no=vnum).count()
    if not vnumtaken:
        return JsonResponse({'vehical_number_error': 'vehical not exits.'})
    return JsonResponse({'vehical_number_valid': True})