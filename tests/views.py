from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
@xframe_options_exempt
def atcoder_badge(request):
    return render(request, 'tests/AtCoderStatuses/badge.html')
