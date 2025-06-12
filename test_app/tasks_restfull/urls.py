from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks_restfull.views import (TaskModelViewSet, TaskReadOnlyModelViewSet, TaskUpdateViewSet, TaskGenerViewSet,
                                   TaskCustomViewSet, TaskCreateViewSet, CustomAuthToken, login, login_jwt)


router = DefaultRouter()
router.register(r'task', TaskModelViewSet, basename='task') # row рядок
router.register(r'task_readonly', TaskReadOnlyModelViewSet, basename='task_readonly')
router.register(r'task_generic', TaskGenerViewSet, basename='task_generic')
router.register(r'task_custom', TaskCustomViewSet, basename='task_custom')
router.register(r'task_create', TaskCreateViewSet, basename='task_create')
router.register(r'task_update', TaskUpdateViewSet, basename='task_viewset')



urlpatterns = [
    path('', include(router.urls)),
    path('token_auth/', CustomAuthToken.as_view(), name='token_auth'),
    path('login/', login, name='login'),
    path('login_jwt/', login_jwt, name='login_jwt'),

]