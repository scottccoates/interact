import logging

from src.apps.read_model.relational.topic.models import TopicLookup

logger = logging.getLogger(__name__)


def save_topic_lookup(id, name, stem, collapsed_stem):
  topic, _ = TopicLookup.objects.update_or_create(id=id,
                                                  defaults=dict(name=name, stem=stem, collapsed_stem=collapsed_stem))

  return topic


def get_topic_lookup(id):
  return TopicLookup.objects.get(id=id)


def get_topic_lookups():
  return TopicLookup.objects.all()
