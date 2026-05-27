from django.views.generic import TemplateView

from apps.core.models import ClientPartnerLogo, ProfileDocument, Testimonial
from apps.projects.models import Project


class HomeView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["featured_projects"] = Project.objects.filter(is_published=True)[:6]
        ctx["testimonials"] = Testimonial.objects.filter(is_published=True)[:12]
        ctx["client_partners"] = ClientPartnerLogo.objects.filter(is_published=True)[:20]
        return ctx


class AboutView(TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile_documents"] = ProfileDocument.objects.filter(is_published=True)[:5]
        return ctx


class TeamView(TemplateView):
    template_name = "core/team.html"


class ContactView(TemplateView):
    template_name = "core/contact.html"
