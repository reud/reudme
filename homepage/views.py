from django.shortcuts import render


# Create your views here.
def homepage(request):
    user = request.GET.get('user', '')
    return render(request, 'homepage/homepage.html')
