from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class ClientCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name, ta_attrs):
    super().__init__()


class ClientAssociatedWithTopic1(DomainEvent):
  event_func_name = 'associated_with_topic_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, relevance, topic_id):
    super().__init__()


class ClientAddedTargetAudienceTopicOption1(DomainEvent):
  event_func_name = 'added_target_audience_topic_option_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name, type, attrs, ta_topic_id, ta_topic_relevance, topic_id):
    super().__init__()


class ClientAddedEngagementAssignment1(DomainEvent):
  event_func_name = 'added_ea_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, attrs, score, score_attrs, prospect_id):
    super().__init__()
