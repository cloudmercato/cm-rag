from django.db import models
from core import querysets


class Provider(models.Model):
    slug = models.CharField(
        verbose_name="slug",
        help_text="Unique ID from Cloud Mercato's database",
        db_index=True,
        primary_key=True,
    )
    name = models.CharField(
        verbose_name="name",
        help_text="As defined by the provider itself",
    )
    short_name = models.CharField(
        verbose_name="name",
        help_text="Made from abreviation or initials.",
    )

    extra = models.JSONField(default=dict)

    objects = querysets.ProviderQuerySet.as_manager()

    def __str__(self):
        return self.name


class Flavor(models.Model):
    provider = models.ForeignKey(
        Provider,
        verbose_name="provider",
        on_delete=models.CASCADE,
    )
    slug = models.CharField(
        db_index=True,
        verbose_name="slug",
        help_text="Unique ID from Cloud Mercato's database",
    )
    name = models.CharField(
        verbose_name="name",
        help_text="As defined by the provider itself",
    )
    cpu = models.PositiveIntegerField(
        verbose_name="CPU",
        help_text="Number of CPU",
    )
    ram = models.PositiveIntegerField(
        verbose_name="RAM",
        help_text="Amount of RAM in MB",
    )

    extra = models.JSONField(default=dict)

    objects = querysets.FlavorQuerySet.as_manager()

    def __str__(self):
        return self.name
