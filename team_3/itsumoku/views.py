from django.shortcuts import render

from itsumoku.app.getmov import exec_getmov


DEFAULT_KEYWORD = 'もくもく会'


def index(request):
    if request.method == 'POST':
        
        during = request.POST['during']
        any = request.POST['keyword']
        male = request.POST['keyword']
        woman = request.POST['keyword']
        anime = request.POST['keyword']

        keyword_list = [DEFAULT_KEYWORD, any, male, woman, anime ]
        keyword = ' '.join(keyword_list)

        context = {
            'df_video_list':  exec_getmov(during, keyword)
        }
        return render(request, 'result.html', context)

    return render(request, 'index.html')


