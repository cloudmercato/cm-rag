from django.db import models
from django_countries.fields import CountryField
from core import querysets


class Provider(models.Model):
    slug = models.CharField(
        max_length=50,
        verbose_name="slug",
        help_text="Unique ID from Cloud Mercato's database",
        db_index=True,
        primary_key=True,
    )
    name = models.CharField(
        max_length=100,
        verbose_name="name",
        help_text="As defined by the provider itself",
    )
    short_name = models.CharField(
        max_length=50,
        verbose_name="short name",
        help_text="Made from abreviation or initials.",
    )
    kind = models.CharField(
        max_length=40,
        null=True, blank=True,
        verbose_name="kind",
        help_text="Main type of cloud service",
    )
    url = models.CharField(
        max_length=150,
        null=True, blank=True,
        verbose_name="URL",
        help_text="Official main URL",
    )
    headquarters = CountryField(
        max_length=2,
        null=True, blank=True,
        verbose_name="headquarters",
        help_text="Origin country in ISO 3166-1 format",
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
        help_text="Provider ID from Cloud Mercato's database",
    )
    slug = models.CharField(
        db_index=True,
        verbose_name="slug",
        help_text="Unique ID from Cloud Mercato's database",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="name",
        help_text="As defined by the provider itself",
    )

    arch = models.CharField(
        max_length=20,
        null=True, blank=True,
        verbose_name="architecture",
        help_text="Architecture powering the CPU",
    )
    type = models.CharField(
        max_length=25,
        null=True, blank=True,
        verbose_name="type",
        help_text="Platform powering the instance",
    )

    cpu = models.PositiveIntegerField(
        verbose_name="CPU",
        help_text="Number of CPU",
    )
    ram = models.PositiveIntegerField(
        verbose_name="RAM",
        help_text="Amount of memory in MB",
    )
    root_volume_size = models.PositiveIntegerField(
        verbose_name="root volume size",
        help_text="Amount of GB if a free root volume is given",
    )
    extra_volume_size = models.PositiveIntegerField(
        verbose_name="extra volume size",
        help_text="Amount of GB if a free extra volume is given",
    )
    gpu = models.PositiveIntegerField(
        verbose_name="GPU",
        help_text="Number of GPU",
    )
    gpu_model = models.CharField(
        max_length=100,
        null=True, blank=True,
        verbose_name="GPU model",
        help_text="Accurate model name as given by hardware vendor",
    )

    max_bandwidth = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="maximum bandwidth",
        help_text="Network bandwidth in GB/month",
    )

    extra = models.JSONField(default=dict)

    objects = querysets.FlavorQuerySet.as_manager()

    def __str__(self):
        return self.name
