from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from tasks.models import Task
from tasks.forms import TaskForm
from tasks.mixins import OwnerOnlyMixin, SuccessMessageMixin, QueryFilterMixin

# @login_required
# def tasks_list(request):
#     tasks = Task.objects.filter(user=request.user)
#     return render(request, 'tasks/tasks_list.html', {'tasks': tasks})

class TaskListView(LoginRequiredMixin, QueryFilterMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = super().get_queryset()
        if self.request.user.is_superuser:
            return tasks
        return tasks.filter(user=self.request.user)

# @login_required
# def create_task(request):
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.user = request.user
#             task.save()
#             return redirect('tasks_list')
#     else:
#         form = TaskForm()
#     return render(request, 'tasks/create_task.html', {'form': form})

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url =  reverse_lazy ('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# @login_required
# def delete_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     if request.method == 'POST':
#         task.delete()
#         return redirect('tasks_list')
#     return render(request, 'tasks/confirm_delete.html')

class TaskDeleteView(LoginRequiredMixin, OwnerOnlyMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/confirm_delete.html'
    success_url = reverse_lazy('task_list')
    pk_url_kwarg = 'pk'
    success_message = "Task deleted successfully."


def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save(update_fields=['completed'])
    return redirect('task_list')
    
    
    
