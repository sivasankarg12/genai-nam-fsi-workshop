from django.urls import path
from core.views import index, short_url
urlpatterns = [
    path('', index, name='index'),
    path('301/<str:id>', short_url, name='redirect'),
]