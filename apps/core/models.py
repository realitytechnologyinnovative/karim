from django.db import models


class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    person_name = models.CharField(max_length=200, blank=True)
    person_title = models.CharField(max_length=200, blank=True)
    quote = models.TextField()
    image = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-updated_at"]

    def __str__(self):
        return self.client_name


class ClientPartnerLogo(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="clients/")
    website = models.URLField(blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class ProfileDocument(models.Model):
    title = models.CharField(max_length=220)
    file = models.FileField(upload_to="profiles/")
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-updated_at"]

    def __str__(self):
        return self.title
