from django.shortcuts import render
from app.getmov import exec_getmov
# Create your views here.
def index(request):
    return render(request, 'index.html')

def form(request):
    return render(request,'form.html')

def result(request):
    # content =exec_getmov(request.POST['during'],request.POST['keyword'])



    return render(request,'result.html')

