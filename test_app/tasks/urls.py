from django.urls import path
from tasks import views as views


urlpatterns = [ 
    path('', views.TaskListView.as_view(), name='task_list'),
    path('create/', views.TaskCreateView.as_view(), name='create_task'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('<int:task_id>/complete/', views.complete_task, name='task_complete'),
]