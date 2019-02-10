from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt


# Create your views here.
@xframe_options_exempt
def atcoder_badge(request):
    user = request.GET.get('user', '')
    return render(request, 'AtCoderStatuses/badge_base.html', {'username': user})
