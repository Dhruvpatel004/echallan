from datetime import *
from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Police
# Create your views here.

# Create your views here.
def index2(request):
    request.session['login'] = False
    return render(request,'police.html')

def policedashboard(request):
    # username=request.POST.get('policeemail','default')
    # password=request.POST.get('policepassword','default')
    # print(username)
    # print(password)
    # username=request.POST.post('rtoemail')
    # password=request.POST.post('rtopassword')

    # cusername=Police.objects.getall(police_username=username,police_password=password)
    # cusername=Police.objects.filter(police_username=username,police_password=password).count()

    # # print(cusername)


    # # if cusername.police_username==username and cusername.police_password==password :
    # if cusername>=1:
    #     send={'user':username,'pass':password}
    #     return render(request,'policedashboard.html',send)

    # else :
    #     return HttpResponse(request,"Wronggggg")
    
    if request.method == 'POST':

        pusername=request.POST.get('policeemail','default')
        ppassword=request.POST.get('policepassword','default')
       

        cusername = Police.objects.filter(police_username=pusername,police_password=ppassword).count()
        
        request.session['loginid'] = pusername
        print(cusername)

        if cusername:
            # police.police_last_login= datetime.now()
            # user = User.objects.get(username=request.user)
            # last_login = police.last_login.strftime('%y-%m-%d %a %H:%M:%S')
            # print(datetime.now())
            user = Police.objects.get(police_username=pusername,police_password=ppassword)
            time=datetime.now()
            print(time)
            user.police_last_login=str(time)
            user.save()
            send = {'user': pusername, 'pass': ppassword}
            request.session['login'] = True
            request.session['username'] = pusername
            # messages.success(request, 'Login successful')
            return render(request, 'policedashboard.html', send)

        else:
            return HttpResponse("Wronggggg")