from django.contrib import admin

from .models import ClientPartnerLogo, ProfileDocument, Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "person_name",
        "person_title",
        "sort_order",
        "is_published",
        "updated_at",
    )
    list_filter = ("is_published",)
    search_fields = ("client_name", "person_name", "person_title", "quote")
    ordering = ("sort_order", "-updated_at")


@admin.register(ClientPartnerLogo)
class ClientPartnerLogoAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order", "is_published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("name",)
    ordering = ("sort_order", "name")


@admin.register(ProfileDocument)
class ProfileDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "sort_order", "is_published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title",)
    ordering = ("sort_order", "-updated_at")
