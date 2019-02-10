from django.shortcuts import render


# Create your views here.
def atcoder_badge(request):
    return render(request, 'tests/AtCoderStatuses/badge.html')
