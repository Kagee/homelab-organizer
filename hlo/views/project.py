from django.views.generic import CreateView, DetailView, ListView, UpdateView

from hlo.models import Project


class ProjectDetailView(DetailView):
    model = Project
    template_name = "project/detail.html"
    context_object_name = "project"

class ProjectListView(ListView):
    model = Project
    template_name = "project/list.html"
    context_object_name = "projects"

class ProjectCreateView(CreateView):
    model = Project
    template_name = "project/form.html"
    context_object_name = "project"

class ProjectUpdateView(UpdateView):
    model = Project
    template_name = "project/form.html"
    context_object_name = "project"
