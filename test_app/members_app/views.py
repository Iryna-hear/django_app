from django.shortcuts import render, redirect
from django.http import HttpResponse
from members_app.models import Members

def page_input(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        request.session['save_input'] = user_input
        return redirect('page_show')
    return render(request, 'members/input.html')

def page_show(request):
    user_input = request.session.get('save_input', '')
    return render(request, 'members/show.html', {'user_input': user_input})

def get_session(request):
    user_session = request.session.get('user_session', 0)
    request.session['user_session'] = user_session + 1
    return HttpResponse(f"user_session: {request.session['user_session']}")

   
def tags_page(request):

    return render(request, 'members/tags.html')
