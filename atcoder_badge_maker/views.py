from django.shortcuts import render

from . import forms


# Create your views here.
def make_form(request):
    form = forms.InputForm(request.GET or None)
    if form.is_valid():
        message = 'htmlを出力しました！'
        state='valid'
    else:
        message = 'AtCoderのニックネームを入力してください。'
        state='invaild'
    return render(request, 'atcoder_badge_maker/form.html', {'message': message, 'form': form,'state':state})
