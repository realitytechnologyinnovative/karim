from django.views.generic import DetailView, ListView

from apps.core.models import ClientPartnerLogo
from apps.projects.models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "projects/projects.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["client_partners"] = ClientPartnerLogo.objects.filter(is_published=True)[:20]
        return ctx


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project_details.html"
    context_object_name = "project"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Project.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["client_partners"] = ClientPartnerLogo.objects.filter(is_published=True)[:20]
        return ctx
