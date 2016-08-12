from django.dispatch import receiver

from src.apps.read_model.key_value.prospect import tasks
from src.domain.prospect.events import ProspectDeleted1, EngagementOpportunityAddedToProfile1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ProspectDeleted1.event_signal)
def execute_prospect_deleted_1(**kwargs):
  pass


@event_idempotent
@receiver(EngagementOpportunityAddedToProfile1.event_signal)
def execute_added_eo_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']

  attrs = event.attrs

  tasks.save_eo_contentent_task.delay(
      event.id, event.external_id,
      event.provider_type, provider_action_type, aggregate_id
  )
