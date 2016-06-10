import logging

from django_rq import job
from rq import get_current_job

from src.domain.prospect import services
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def save_prospect_from_provider_info_task(provider_external_id, provider_type):
  log_message = ("provider_external_id: %s, provider_type: %s", provider_external_id, provider_type)

  with log_wrapper(logger.info, *log_message):
    return services.get_prospect_id_from_provider_info_(provider_external_id, provider_type)


@job('default')
def save_profile_from_provider_info_chain(provider_external_id, provider_type):
  job = get_current_job()
  prospect_id = job.dependency.result
  # queue up this job now because we want to store the prospect id (result of previous job) before that job's TTL
  # expires
  save_profile_from_provider_info_task.delay(prospect_id, provider_external_id, provider_type)


@job('default')
def save_profile_from_provider_info_task(prospect_id, provider_external_id, provider_type):
  log_message = (
    "prospect_id: %s, provider_external_id: %s, provider_type: %s",
    prospect_id, provider_external_id, provider_type
  )

  with log_wrapper(logger.info, *log_message):
    return services.get_profile_id_from_provider_info(prospect_id, provider_external_id, provider_type)


@job('high')
def save_profile_lookup_by_provider_task(profile_id, provider_external_id, provider_type, prospect_id):
  log_message = (
    "profile_id: %s, provider_external_id: %s, provider_type: %s",
    prospect_id, provider_external_id, provider_type
  )

  with log_wrapper(logger.info, *log_message):
    return services.save_profile_lookup_by_provider(profile_id, provider_external_id, provider_type, prospect_id)
