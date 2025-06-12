from django.http import HttpResponseNotAllowed
from django.contrib import messages




class OwnerOnlyMixin:
   def dispatch(self, request, *args, **kwargs):
       obj = self.get_object()
       if obj.user != request.user:
           return HttpResponseNotAllowed("You do not have permission to access this object.")
       return super().dispatch(request, *args, **kwargs)
   

class SuccessMessageMixin:
    success_message = "Operation was successful."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
    

class QueryFilterMixin:
    filter_p = 'completed'

    def get_queryset(self):
        qs = super().get_queryset()
        filter_value = self.request.GET.get(self.filter_p)
        if filter_value and filter_value.lower() == 'true':
            return qs.filter(completed=True)
        elif filter_value and filter_value.lower() == 'false':
            return qs.filter(completed=False)
        return qs



 

    


    
