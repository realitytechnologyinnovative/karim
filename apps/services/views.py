from django.views.generic import ListView

from apps.services.models import Service


class ServiceListView(ListView):
    model = Service
    template_name = "services/services.html"
    context_object_name = "services"

    def get_queryset(self):
        return Service.objects.filter(is_published=True).order_by("sort_order", "title")
