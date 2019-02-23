from django.urls import path

from . import views

urlpatterns = [
    path('callback', views.callback, name='callback'),
    path('push', views.push_message_from_model, name='push'),

]
