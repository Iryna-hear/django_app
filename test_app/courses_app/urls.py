from django.urls import path
from .views import courses_page

urlpatterns = [
    path('', courses_page, name='courses_page'),
]