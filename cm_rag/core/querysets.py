import pandas as pd
from django.db import models
from core import files


class QuerySet(models.QuerySet):
    @property
    def files(self):
        return files.FileManager()

    def filter_instance(self, row):
        """Filter unique ID(s) from a row"""
        raise NotImplementedError("Not implemented")

    def create_values_from_row(self, row):
        model_fields = [f.name for f in self.model._meta.fields]
        values = {
            k: v for k, v in dict(row).items()
            if k in model_fields
        }
        return values

    def refresh(self):
        filename = self.files.make_filename(self.model._meta.model_name)
        df = pd.read_csv(filename)
        df.columns = [c.lower().replace(' ', '_') for c in df.columns]

        for idx, row in df.iterrows():
            instance_ = self.filter_instance(row)
            values = self.create_values_from_row(row)
            if not instance_.exists():
                self.model.objects.create(**values)
            else:
                instance_.update(**values)


class ProviderQuerySet(QuerySet):
    def filter_instance(self, row):
        instance_ = self.model.objects.filter(slug=row.slug)
        return instance_


class FlavorQuerySet(QuerySet):
    def filter_instance(self, row):
        instance_ = self.model.objects.filter(
            provider=row.provider_slug,
            slug=row.slug,
        )
        return instance_

    def create_values_from_row(self, row):
        values = super().create_values_from_row(row)
        values.pop('provider')
        values.update(
            provider_id=row.provider_slug,
        )
        return values
