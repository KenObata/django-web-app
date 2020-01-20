from django.shortcuts import render
from django.views.generic import (View,TemplateView,ListView,DetailView
                                  ,CreateView,UpdateView,DeleteView)

"""
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')


class CBView(View):
    def get(self, request):
        return HttpResponse("Class Based View is cool")
"""
# Create your views here.
class IndexView(TemplateView):
    #if folder structure is basic_app/index.html,
    # then template_name ='basic_app/index.html'
    template_name = 'index.html'

"""
    # **kwargs = key word arg
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['injectme'] = 'This is from views.py Baseic Injection'
        return context
"""

from basic_app import models
from django.urls import reverse_lazy # for DeleteView

class SchoolListView(ListView):
    model = models.School
    context_object_name='schools'
    # school_list

class SchoolDetailView(DetailView):
    context_object_name='school_detail'
    model = models.School
    template_name = 'basic_app/school_detail.html'

class SchoolCreateView(CreateView):
    model = models.School
    fields=('name','principal','location')
#context_object_name='create'

class SchoolUpdateView(UpdateView):
    fields = ("name","principal")
    model = models.School

class SchoolDeleteView(DeleteView):
    model = models.School
    success_url = reverse_lazy("basic_app:list")
