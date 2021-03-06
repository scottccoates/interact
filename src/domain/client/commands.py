from src.libs.common_domain.command_signal import CommandSignal
from src.libs.common_domain.domain_command import DomainCommand
from src.libs.python_utils.objects.object_utils import initializer


class CreateClient(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, name, ta_attrs):
    pass


class AssociateWithTopic(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, relevance, topic_id):
    pass


class AddTopicOption(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, name, type, attrs, ta_topic_id):
    pass


class AddEaBatch(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, batch_id, batch_eas):
    pass
