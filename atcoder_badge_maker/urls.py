from django.urls import path

from . import views

urlpatterns = [
    path('', views.make_form, name='atcoder_badge_maker'),

]
