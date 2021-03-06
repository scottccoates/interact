from django.db import models

from src.apps.read_model.relational.models import ReadModel


class ProfileLookupByProvider(ReadModel):
  external_id = models.CharField(max_length=2400)
  provider_type = models.CharField(max_length=2400)
  prospect_id = models.CharField(max_length=8)

  class Meta:
    unique_together = ("external_id", "provider_type")

  def __str__(self):
    return 'ProfileLookupByProvider {id}: {provider_type}'.format(id=self.id, provider_type=self.provider_type)


class EoLookupByProvider(ReadModel):
  external_id = models.CharField(max_length=2400)
  provider_type = models.CharField(max_length=2400)
  prospect_id = models.CharField(max_length=8)

  # this will prevent duplicate EO's within same prospect boundary - in case multiple eo's come in concurrently
  class Meta:
    unique_together = ("external_id", "provider_type", "prospect_id")

  def __str__(self):
    return 'EoLookupByProvider {id}: {provider_type}'.format(id=self.id, provider_type=self.provider_type)
