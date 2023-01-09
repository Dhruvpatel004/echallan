from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def index(request):

    return render(request,'index.html')

def user(request):
    ab=request.GET.get('vehicleNumber','default')
    # ab=request.GET.get("text1",'default')
    b={"a":ab}
    return render(request,"user.html",b)