from django.urls import path
from .views import page_input, page_show, get_session


urlpatterns = [
    path('input/', page_input, name='page_input'),
    path('show/', page_show, name='page_show'),
    path('session/', get_session, name='get_session'),
]