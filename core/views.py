from django.http import HttpResponseRedirect
from django.utils.translation import activate


# Til o'zgartirish uchun funksiya
def set_language(request):
    if request.method == 'POST' and 'language' in request.POST:
        language = request.POST['language']
        response = HttpResponseRedirect(request.POST.get('next', '/'))
        response.set_cookie('selected_language', language)
        activate(language)
        return response
    return HttpResponseRedirect('/')
