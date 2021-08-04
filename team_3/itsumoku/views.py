from django.shortcuts import render
from itsumoku.app.getmov import exec_getmov
import datetime
def index(request):
        return render(request, 'index.html')


def result(request):
    if request.method == 'POST':
        
        during = request.POST['during']
        during =int(during)*60
        keyword = request.POST['keyword']
        
        context = {
            'df_video_list':  exec_getmov(during, keyword)
        }
        return render(request, 'result.html', context)

    return render(request,'index.html')
    


        




