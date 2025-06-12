from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.contrib import messages
from tasks.models import Task, TaskLog


@receiver(post_save, sender=Task)
def notify_task_completed(sender, instance, created, update_fields, **kwargs):
    request = kwargs.get('request')
    if request and not created and update_fields and 'completed' in update_fields and instance.completed:
            messages.success(request, f'Task "{instance.title}" has been marked as completed.')


@receiver(pre_delete, sender=Task)
def notify_task_deleted(sender, instance, **kwargs):
    if instance.id == 4:
        raise Task.DoesNotExist("Task with ID 4 cannot be deleted.")
    TaskLog.objects.create(
       action=TaskLog.DELETE,
       user=instance.user,
   )
   