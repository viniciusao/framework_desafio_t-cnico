from django.urls import path

from .views import retrieve_topmost


urlpatterns = [
    path('', retrieve_topmost, name='retrieve_topmost')
]