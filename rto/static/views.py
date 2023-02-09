

# Create your views here.

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .models import RTOadmin
from datetime import *
from police.models import Police

# Create your views here.
def authcheck(request):
    if request.session.get('login') == False or request.session.get('username') == None:
            # messages.success(request, 'Login needed')
            return False
    else :
        return True

def user(request):
    
    user_info={
        'username':request.session.get('username')
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
        # RTOadmin.admin_created_date=datetime.date
        # RTOadmin.admin_username='OK'
        # RTOadmin.admin_password='OK'
        # RTOadmin.add_to_class['admin_username':123]
        # RTOadmin.save()
    # username=request.POST.post('rtoemail')
    # password=request.POST.post('rtopassword')

        cusername = RTOadmin.objects.filter(
        admin_username=username, admin_password=password).count()
        request.session['loginid'] = username
        print(cusername)

        if cusername:
            request.session['login'] = True
            request.session['username'] = username

            context = {
            'user': user(request),
            }
            return render(request, 'rtodashboard.html', context)

        else:
            return HttpResponse("Wronggggg")

    else:
        if request.session.get('login') == False or request.session.get('username') == None:
            # messages.success(request, 'Login needed')
            return redirect('/rto-administrator/')

        else:
            context = {
            'user': user(request),
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

            police = Police(police_username=p_username, police_password=p_password, police_created_date=datetime.today(),
                        police_firstname=p_fname, police_lastname=p_lname,
                        police_age=p_age, police_birth_date=date_of_birth, police_joing_date=date_of_join,
                        police_address=p_address, police_gender=p_gender, police_last_login=p_last_log)
            police.save()
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
        return render(request, 'rto_police_list.html',context)

    else:
        return log_rto(request)



def delete_pid(request, pid):
    if  authcheck(request):
        # pid=request.GET.get('pid','default')
        # pid=request.GET.get('pid')
        police = Police.objects.get(police_id=pid)
        police.delete()
        return redirect('../')

    else:
        return log_rto(request)


def delete_pid(request, pid):
    if authcheck(request):

        # pid=request.GET.get('pid','default')
        # pid=request.GET.get('pid')
        police = Police.objects.get(police_id=pid)
        police.delete()
        return redirect('../')

    else:
        return log_rto(request)


def update_pid(request, pid):

    if authcheck(request):
        police = Police.objects.get(police_id=pid)
    

        context = {
            'user': user(request),
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
            member.police_username=p_username
            member.police_password=p_password
            member.police_firstname=p_fname
            member.police_lastname=p_lname
            member.police_age=p_age
            member.police_birth_date=date_of_birth
            member.police_joing_date=date_of_join
            member.police_address=p_address
            member.police_gender=p_gender
            member.save()
    
        return redirect('../../')
    else:
        return log_rto


def addpo(request):
    if authcheck(request):
        #   police = Police.objects.get(police_id=pid)

        #   context = {
        #     'member': police
        #   }

        context = {
            'user': user(request),
            # 'p': allpoli
        }
        return render(request, 'rto_add_police.html',context)

    else:
        return log_rto(request)
