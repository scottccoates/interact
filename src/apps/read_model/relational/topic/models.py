from django.db import models

from src.apps.read_model.relational.models import ReadModel


class TopicLookup(ReadModel):
  name = models.CharField(max_length=2400)
  stem = models.CharField(max_length=2400)
  collapsed_stem = models.CharField(max_length=2400)

  def __str__(self):
    return 'TopicLookup {id}: {name}'.format(id=self.id, name=self.name)
