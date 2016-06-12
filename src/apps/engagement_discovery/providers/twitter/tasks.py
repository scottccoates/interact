import logging

from django_rq import job

from src.apps.engagement_discovery.providers.twitter.service import \
  discover_engagement_opportunities_from_twitter_ta_topic_option
from src.apps.relational.client import service as client_service
from src.domain.common import constants

logger = logging.getLogger(__name__)


@job('default')
def discover_engagement_opportunities_from_twitter_ta_topics_task(**kwargs):
  discover = discover_engagement_opportunities_from_twitter_ta_topic_option_task

  ta_topic_options_to_run = client_service.get_active_ta_topic_options(). \
    filter(option_type=constants.TopicOptionType.TWITTER_SEARCH)

  for ta_topic_option in ta_topic_options_to_run:
    discover.delay(ta_topic_option.id, **kwargs)


@job('default')
def discover_engagement_opportunities_from_twitter_ta_topic_option_task(ta_topic_option_id, **kwargs):
  ta_topic_option = client_service.get_ta_topic_option(ta_topic_option_id)
  return discover_engagement_opportunities_from_twitter_ta_topic_option(ta_topic_option, **kwargs)
