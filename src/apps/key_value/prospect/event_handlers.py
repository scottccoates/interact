from django.dispatch import receiver

from src.apps.key_value.prospect import tasks
from src.domain.prospect.events import ProspectDeleted1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ProspectDeleted1.event_signal)
def execute_prospect_deleted_1(**kwargs):
  prospect_id = kwargs['aggregate_id']

  tasks.add_prospect_to_deleted_set_task.delay(prospect_id)
