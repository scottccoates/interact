import logging

from django_rq import job

from src.apps.read_model.graph.prospect import service
from src.domain.prospect.service import prospect_is_deleted
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def create_prospect_in_graphdb_task(prospect_id):
  return service.create_prospect_in_graphdb(prospect_id)['id']


@job('default')
def delete_prospect_in_graphdb_task(prospect_id):
  return service.delete_prospect_in_graphdb(prospect_id)


@job('default')
def create_profile_in_graphdb_task(prospect_id, profile_id):
  return service.create_profile_in_graphdb(prospect_id, profile_id)['id']


@job('default')
def create_eo_in_graphdb_task(prospect_id, profile_id, eo_id, topic_ids):
  log_message = ("id: %s", prospect_id)

  with log_wrapper(logger.info, *log_message):
    if prospect_is_deleted(prospect_id):
      logger.info('prospect %s is deleted. aborting task', prospect_id)
    else:
      return service.create_eo_in_graphdb(profile_id, eo_id, topic_ids)['id']
