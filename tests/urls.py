from django.urls import path

from . import views

urlpatterns = [
    path('AtCoder_badges/', views.atcoder_badge, name='atcoder_badge'),

]
