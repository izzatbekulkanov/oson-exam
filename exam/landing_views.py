from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.



def about_me(request):
    return render(request, 'landing/menu/about_me.html')



def social(request):
    return render(request, 'landing/menu/social.html')



def contact_me(request):
    return render(request, 'landing/menu/contact_me.html')
