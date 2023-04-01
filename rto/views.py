

# Create your views here.

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .models import Challan, RTOadmin ,  Vehicle , Rules
from datetime import *
from police.models import Police
import json
from django.http import JsonResponse

# Create your views here.
def authcheck(request):
    if request.session.get('login') == False or request.session.get('username') == None:
        # messages.success(request, 'Login needed')
        return False
    else:
        return True


def user(request):

    user_info = {
        'username': request.session.get('username')
    }

    return user_info


def index(request):
    request.session['login'] = False
    request.session['username'] = None
    return render(request, 'rto.html')


def rtodashboard(request):
    if request.method == 'POST':

        username = request.POST.get('rtoemail', 'default')
        password = request.POST.get('rtopassword', 'default')

        cusername = RTOadmin.objects.filter(admin_username=username, admin_password=password).count()
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
        tallchs = list(Challan.objects.filter(offence_date=datetime.now().date()).values())
        yallchs = list(Challan.objects.filter(offence_date=yesterday).values())

        sumallchs = list(Challan.objects.filter(offence_date=datetime.now().date()))
        yesterdaysumallchs = list(Challan.objects.filter(offence_date=yesterday))

        nowtotalchs = list(Challan.objects.filter(offence_date__gte=monthbefore,offence_date__lte=datetime.now().date()))
        lasttotalchs = list(Challan.objects.filter(offence_date__gte=monthbeforebefore,offence_date__lte=monthbefore))

        paidtotalchs = list(Challan.objects.filter(offence_date__gte=monthbefore,offence_date__lte=datetime.now().date()).filter(status="Paid"))
        pendingtotalchs = list(Challan.objects.filter(offence_date__gte=monthbefore,offence_date__lte=datetime.now().date()).filter(status="Pending"))

        
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
        # challan_difference_day=

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




            return render(request, 'rtodashboard.html', context)

        else:
            messages.warning(request, 'Invalid Credentials')
            return redirect('../')

    else:
        if request.session.get('login') == False or request.session.get('username') == None:
            # messages.success(request, 'Login needed')
            return redirect('/rto-administrator/')

        else:
            username = request.POST.get('rtoemail', 'default')
            password = request.POST.get('rtopassword', 'default')
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
            tallchs = list(Challan.objects.filter(offence_date=datetime.now().date()).values())
            yallchs = list(Challan.objects.filter(offence_date=yesterday).values())

            sumallchs = list(Challan.objects.filter(offence_date=datetime.now().date()))
            yesterdaysumallchs = list(Challan.objects.filter(offence_date=yesterday))

            nowtotalchs = list(Challan.objects.filter(offence_date__gte=monthbefore,offence_date__lte=datetime.now().date()))
            lasttotalchs = list(Challan.objects.filter(offence_date__gte=monthbeforebefore,offence_date__lte=monthbefore))

            paidtotalchs = list(Challan.objects.filter(offence_date__gte=monthbefore,offence_date__lte=datetime.now().date()).filter(status="Paid"))
            pendingtotalchs = list(Challan.objects.filter(offence_date__gte=monthbefore,offence_date__lte=datetime.now().date()).filter(status="Pending"))

        
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
        # challan_difference_day=

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
            # if cusername:
            # request.session['login'] = True
            # request.session['username'] = username

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
            
            return render(request, 'rtodashboard.html', context)

def addp(request):
    if authcheck(request):
        if request.method == "POST":
            # user_name = request.POST.get('uname')
            # password = request.POST.get('passp')
            p_username = request.POST.get('p_username')
            p_password = request.POST.get('p_password')
            p_fname = request.POST.get('p_fname')
            p_lname = request.POST.get('p_lname')
            p_age = request.POST.get('p_age')
            date_of_birth = request.POST.get('date_of_birth')
            date_of_join = request.POST.get('date_of_join')
            p_address = request.POST.get('p_address')
            p_gender = request.POST.get('p_gender')
            p_last_log = 'not yet'

            userexist = Police.objects.filter(police_username=p_username).count()

            if userexist:
                messages.warning(request, 'Account is alredy Created')
                return redirect('../')


            else:
                police = Police(police_username=p_username, police_password=p_password, police_created_date=datetime.today(),
                            police_firstname=p_fname, police_lastname=p_lname,
                            police_age=p_age, police_birth_date=date_of_birth, police_joing_date=date_of_join,
                            police_address=p_address, police_gender=p_gender, police_last_login=p_last_log)
                police.save()
                messages.success(request, 'Account is Created Successfully!')
        # messages.success(request, 'Your message has been sent!')
                return redirect('../')

    else:
        return log_rto(request)


def log_rto(request):
    request.session['login'] = False
    request.session['username'] = None
    return redirect('/rto-administrator/')


def allp(request):
    if authcheck(request):
        allpoli = list(Police.objects.all().values())
        # print(allpoli)
        u = request.session.get('username')

        context = {
            'user': user(request),
            'p': allpoli
        }

        # return render(request, 'p.html', ab)
        return render(request, 'rto_police_list.html', context)

    else:
        return log_rto(request)

# def delete_pid(request, pid):
#     if authcheck(request):
#         # pid=request.GET.get('pid','default')
#         # pid=request.GET.get('pid')
#         police = Police.objects.get(police_id=pid)
#         police.delete()
#         return redirect('../')

#     else:
#         return log_rto(request)


def delete_pid(request, pid):
    if authcheck(request):

        # pid=request.GET.get('pid','default')
        # pid=request.GET.get('pid')
        police = Police.objects.get(police_id=pid)
        p_username=police.police_username
        police.delete()
        messages.warning(request, 'Account - '+str(p_username) +' is Deleted Successfully!')
        return redirect('../')

    else:
        return log_rto(request)


def update_pid(request, pid):

    if authcheck(request):
        police = Police.objects.get(police_id=pid)

        context = {
            'user': user(request),
            'member': police,
            'access':True
        }
        return render(request, 'update_police.html', context)

    else:
        return log_rto()
    
def show_pid(request, pid):

    if authcheck(request):
        police = Police.objects.get(police_id=pid)

        context = {
            'user': user(request),
            'member': police,
            'access':False
        }
        return render(request, 'update_police.html', context)

    else:
        return log_rto()


def update_pid_record(request, pid):
    if authcheck(request):
        if request.method == "POST":
            # user_name = request.POST.get('uname')
            # password = request.POST.get('passp')
            p_username = request.POST.get('p_username')
            p_password = request.POST.get('p_password')
            p_fname = request.POST.get('p_fname')
            p_lname = request.POST.get('p_lname')
            p_age = request.POST.get('p_age')
            date_of_birth = request.POST.get('date_of_birth')
            date_of_join = request.POST.get('date_of_join')
            p_address = request.POST.get('p_address')
            p_gender = request.POST.get('p_gender')

            member = Police.objects.get(police_id=pid)
            member.police_username = p_username
            member.police_password = p_password
            member.police_firstname = p_fname
            member.police_lastname = p_lname
            member.police_age = p_age
            member.police_birth_date = date_of_birth
            member.police_joing_date = date_of_join
            member.police_address = p_address
            member.police_gender = p_gender
            member.save()
        messages.success(request, 'Account - '+str(p_username) +' is Updated Successfully!')
        return redirect('../../')
    else:
        return log_rto


def addpo(request):
    if authcheck(request):

        context = {
            'user': user(request),
            # 'p': allpoli
        }
        return render(request, 'rto_add_police.html', context)

    else:
        return log_rto(request)

#                       #
# vehical side function #
#                       #

def addv(request):
    if authcheck(request):
        if request.method == "POST":
            v_no = request.POST.get('v_no')
            v_own_name = request.POST.get('v_own_name')
            v_own_conno = request.POST.get('v_own_conno')
            v_own_email = request.POST.get('v_own_email')
            v_com_name = request.POST.get('v_com_name')
            v_own_address = request.POST.get('v_own_address')
            # v_class = request.POST.get('v_class')
            v_date_reg = request.POST.get('v_date_reg')
            v_chass_no = request.POST.get('v_chass_no')
            v_eng_no = request.POST.get('v_eng_no')
            v_own_srno = request.POST.get('v_own_srno')
            v_fuel = request.POST.get('v_fuel')
            v_seat = request.POST.get('v_seat')
            v_model_name = request.POST.get('v_model_name')
            v_user_last_log = 'not yet'

            vexist = Vehicle.objects.filter(vehicle_no=v_no).count()
            if vexist:
                messages.warning(request, 'Vehicle is alredy Registered')
                return redirect('../')

            else:
                a=Vehicle(vehicle_no=v_no,vehicle_own_name=v_own_name,vehicle_own_contact=v_own_conno,vehicle_own_add=v_own_address,vehicle_own_email=v_own_email,vehicle_company_name=v_com_name,vehicle_date_reg=v_date_reg,vehicle_chassics_no=v_chass_no,vehicle_eng_no=v_eng_no,vehicle_own_srno=v_own_srno,vehicle_fuel_use=v_fuel,vehicle_Seat_cap=v_seat,vehicle_model_name=v_model_name,vehicle_last_login=v_user_last_log,vehicle_created_date=date.today())
                a.save()
                messages.success(request, 'Vehicle is Register Successfully!')
                # messages.success(request, 'Your message has been sent!')
                return redirect('../')
            
    else:
        return log_rto(request)
    
def addve(request):
    if authcheck(request):
        context = {
            'user': user(request),
        }
        return render(request, 'rto_add_vehicle.html',context)
    else:
        return log_rto(request)

def allv(request):
    if authcheck(request):
        allvehicle = list(Vehicle.objects.all().values())
        # print(allpoli)
        # u = request.session.get('username')
        context = {
            'user': user(request),
            'p': allvehicle
            }

        # return render(request, 'p.html', ab)
        return render(request, 'rto_vehicle_list.html',context)
    else:
        return log_rto(request)
    
def delete_vid(request, vid):
    if authcheck(request):

        # pid=request.GET.get('pid','default')
        # pid=request.GET.get('pid')
        vehicle = Vehicle.objects.get(vehicle_id=vid)
        vehicle_no=vehicle.vehicle_no
        vehicle.delete()
        messages.warning(request, ' Vehicle no : - '+str(vehicle) +' is Deleted Successfully!')
        return redirect('../')
    else:
        return log_rto(request)

def update_vid(request, vid):

    if authcheck(request):
        vehicle = Vehicle.objects.get(vehicle_id=vid)
    
        context = {
            'user': user(request),
            'member':vehicle,
            'access':True

            }
        return render(request, 'update_vehicle.html', context)
    
    else:
        return log_rto()
    
def show_vid(request, vid):

    if authcheck(request):
        vehicle = Vehicle.objects.get(vehicle_id=vid)
    
        context = {
            'user': user(request),
            'member':vehicle,
            'access':False

            }
        return render(request, 'update_vehicle.html', context)
    
    else:
        return log_rto()
  

def update_vid_record(request, vid):
    if authcheck(request):
        if request.method == "POST":
            v_no = request.POST.get('v_no')
            v_own_name = request.POST.get('v_own_name')
            v_own_conno = request.POST.get('v_own_conno')
            v_own_email = request.POST.get('v_own_email')
            v_com_name = request.POST.get('v_com_name')
            v_own_address = request.POST.get('v_own_address')
            # v_class = request.POST.get('v_class')
            v_date_reg = request.POST.get('v_date_reg')
            v_chass_no = request.POST.get('v_chass_no')
            v_eng_no = request.POST.get('v_eng_no')
            v_own_srno = request.POST.get('v_own_srno')
            v_fuel = request.POST.get('v_fuel')
            v_seat = request.POST.get('v_seat')
            v_model_name = request.POST.get('v_model_name')

            member = Vehicle.objects.get(vehicle_id=vid)
            member.vehicle_no=v_no
            member.vehicle_own_name=v_own_name
            member.vehicle_own_contact=v_own_conno
            member.vehicle_own_email=v_own_email
            member.vehicle_company_name=v_com_name
            member.vehicle_own_add=v_own_address
            member.vehicle_date_reg=v_date_reg
            member.vehicle_chassics_no=v_chass_no
            member.vehicle_eng_no=v_eng_no
            member.vehicle_own_srno=v_own_srno
            member.vehicle_fuel_use=v_fuel
            member.vehicle_Seat_cap=v_seat
            member.vehicle_model_name=v_model_name
            member.save()
        messages.success(request, 'Vehicle - '+str(v_no) +' is Updated Successfully!')
        return redirect('../../')
    else:
        return log_rto

#                       #
# Rule side function    #
#                       #

def addrl(request):
    if authcheck(request):
        if request.method == "POST":
            rule_code= request.POST.get('rule_code')
            rule_desc = request.POST.get('dec_off')
            rule_sect = request.POST.get('Sect')
            rule_pen = request.POST.get('penalty')
            
            rexist = Rules.objects.filter(rule_code=rule_code).count()
            if rexist:
                messages.warning(request, 'Rule is alredy Created')
                return redirect('../')
            else:
                rule = Rules(rule_code=rule_code,rule_desc=rule_desc, rule_sect=rule_sect,rule_pen=rule_pen)
                rule.save()
                messages.success(request, 'Rule is Created Successfully!')
        # messages.success(request, 'Your message has been sent!')
                return redirect('../')
    else:
        return log_rto(request)


def addr(request):
    if authcheck(request):
        context = {
            'user': user(request),
        }
        return render(request, 'rto_add_rule.html',context)
    else:
        return log_rto(request)

#html is not made yet
def allrule(request):
    if authcheck(request):
        allrule = list(Rules.objects.all().values())
        # print(allpoli)
        # u = request.session.get('username')
        context = {
            'user': user(request),
            'r': allrule
            }

        # return render(request, 'p.html', ab)
        return render(request, 'rto_rule_list.html',context)
    else:
        return log_rto(request)

def delete_rid(request, rid):
    if authcheck(request):

        # pid=request.GET.get('pid','default')
        # pid=request.GET.get('pid')
        rule = Rules.objects.get(rule_id=rid)
        rule_code=rule.rule_code
        rule.delete()
        messages.warning(request, ' RULE : - '+str(rule_code) +' is Deleted Successfully!')
        return redirect('../')

    else:
        return log_rto(request)
    
def update_rid(request, rid):

    if authcheck(request):
        rule = Rules.objects.get(rule_id=rid)
        context = {
            'user': user(request),
            'member':rule,
            'access':True
            }
        return render(request, 'update_rule.html', context)
    
    else:
        return log_rto()
    
def show_rid(request, rid):

    if authcheck(request):
        rule = Rules.objects.get(rule_id=rid)

        context = {
            'user': user(request),
            'member': rule,
            'access':False
        }
        return render(request, 'update_rule.html', context)

    else:
        return log_rto()


    
def update_rid_record(request, rid):
    if authcheck(request):
        if request.method == "POST":
            rule_code = request.POST.get('rule_code')
            rule_desc = request.POST.get('rule_desc')
            rule_sect = request.POST.get('rule_sect')
            rule_pen = request.POST.get('rule_pen')

            rule = Rules.objects.get(rule_id=rid)
            rule.rule_code=rule_code
            rule.desc=rule_desc
            rule.sect=rule_sect
            rule.rule_pen=rule_pen
     
            rule.save()
        messages.success(request, 'Rule  - '+str(rule_code) +' is Updated Successfully!')
        return redirect('../../')
    else:
        return log_rto


def upcoming(request):

    if authcheck(request):
        context = {
            'user': user(request),
        }
        return render(request, 'c.html', context)

    else:
        return log_rto()
    
def profile(request):

    if authcheck(request):
        context = {
            'user': user(request),
        }
        return render(request, 'profile.html', context)

    else:
        return log_rto()

def changepassword(request):

    if authcheck(request):
        
        if request.method == "POST":
            cpassword = request.POST.get('password')
            npassword = request.POST.get('newpassword')
            renpassword= request.POST.get('renewpassword')
            username= request.POST.get('rtousername')

            print("C  : ",cpassword)
            print("n  : " ,npassword)
            print("RN : ",renpassword)
            if npassword != renpassword:
                messages.warning(request, 'New password does not match with re-enterd password')
            else:
                rto = RTOadmin.objects.get(admin_username=username)
                print(rto.admin_password)
                print(cpassword)
                if rto.admin_password==cpassword:
                    rto.admin_password=npassword
                    rto.save()
                    messages.success(request, 'Password is changed successfuly ')
                
                else:
                    messages.warning(request, 'Current password does not match.')
                    
        return redirect('../')
    else:
        return log_rto()




#                           #
#server Api Start From here`#
#                           #
#
def validate_username_api(request):
    data = json.loads(request.body)
    username = data['username']

    usernametaken = Police.objects.filter(police_username=username).count()
    if usernametaken:
        return JsonResponse({'username_error': 'username already in use.'})
    return JsonResponse({'username_valid': True})

def validate_vehical_number_api(request):
    data = json.loads(request.body)
    vnum = data['vehical_number']

    vnumtaken = Vehicle.objects.filter(vehicle_no=vnum).count()
    if vnumtaken:
        return JsonResponse({'vehical_number_error': 'vehical number already taken.'})
    return JsonResponse({'vehical_number_valid': True})

def validate_vehical_engine_number_api(request):
    data = json.loads(request.body)
    v_e_num = data['vehical_engine_number']

    v_e_numtaken = Vehicle.objects.filter(vehicle_eng_no=v_e_num).count()
    if v_e_numtaken:
        return JsonResponse({'vehical_engine_number_error': 'vehical engine number already taken.'})
    return JsonResponse({'vehical_engine_number_valid': True})

def validate_vehical_chassics_number_api(request):
    data = json.loads(request.body)
    v_c_num = data['vehical_chassics_number']

    v_c_numtaken = Vehicle.objects.filter(vehicle_chassics_no=v_c_num).count()
    if v_c_numtaken:
        return JsonResponse({'vehical_chassics_number_error': 'vehical chassics number already taken.'})
    return JsonResponse({'vehical_chassics_number_valid': True})

def validate_rule_code_api(request):
    data = json.loads(request.body)
    rcode= data['rule_code']

    rcode_taken = Rules.objects.filter(rule_code=rcode).count()
    if rcode_taken:
        return JsonResponse({'rule_code_error': 'rule code already used.'})
    return JsonResponse({'rule_code': True})

def allcrto(request):
    if authcheck(request):
        allchs = list(Challan.objects.all().values().reverse())
        # allchs = list(Vehicle.objects.all().values())
        # print(allpoli)
        allchs=allchs[::-1]
        c = request.session.get('username')
        v = request.session.get('username')
 
        context1 = {
            'user': user(request),
            'c': allchs                    
            }
        return render(request, 'challan_history.html',context1)

    else:
        return log_rto(request)
    

def rchallan(request,cno):
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
        return render(request, 'rchallan.html', context)
    else:
        return log_rto()