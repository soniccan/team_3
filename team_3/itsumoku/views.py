from django.shortcuts import render


from itsumoku.app.getmov import exec_getmov


DEFAULT_KEYWORD = 'もくもく会'


def index(request):
    if request.method == 'POST':
        
        during = request.POST['during']
        keyword = request.POST['keyword']

        context = {
            'df_video_list':  exec_getmov(during, keyword)
        }
        return render(request, 'result.html', context)
    
    return render(request, 'form.html')

def form(request):
    return render(request, 'form.html')




