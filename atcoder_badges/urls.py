from django.urls import path

from . import views

urlpatterns = [
    path('', views.atcoder_badge, name='atcoder_badge'),

]
