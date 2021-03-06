from django.core.exceptions import ObjectDoesNotExist

from src.apps.read_model.relational.prospect.service import get_profile_lookup_from_provider_info, \
  get_engagement_opportunity_lookup_from_provider_info
from src.domain.prospect.commands import CreateProspect, AddProfile, AddEO, MarkProspectAsDuplicate, \
  ConsumeDuplicateProspect
from src.domain.prospect.entities import Prospect
from src.domain.prospect.exceptions import DuplicateProspectError
from src.libs.common_domain import dispatcher, aggregate_repository
from src.libs.python_utils.id.id_utils import generate_id


def populate_prospect_id_from_provider_info_(external_id, provider_type, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  try:
    profile = get_profile_lookup_from_provider_info(external_id, provider_type)
    prospect_id = profile.prospect_id
  except ObjectDoesNotExist:
    # at some point in the future,  we could get initial prospect info from a 3rd party api. We could get email
    # addresses, etc.
    prospect_id = generate_id()
    create_prospect = CreateProspect(prospect_id, {}, [])
    _dispatcher.send_command(-1, create_prospect)

  return prospect_id


def populate_profile_id_from_provider_info(prospect_id, external_id, provider_type, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  try:
    profile = get_profile_lookup_from_provider_info(external_id, provider_type)

    if prospect_id != profile.prospect_id:
      raise DuplicateProspectError(profile.prospect_id, prospect_id)

    profile_id = profile.id

  except (ObjectDoesNotExist, DuplicateProspectError):

    profile_id = generate_id()

    create_profile = AddProfile(profile_id, external_id, provider_type)

    _dispatcher.send_command(prospect_id, create_profile)

  return profile_id


def populate_engagement_opportunity_id_from_engagement_discovery(profile_id,
                                                                 prospect_id, engagement_opportunity_discovery_object,
                                                                 _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  discovery = engagement_opportunity_discovery_object

  provider_type = discovery.provider_type

  try:
    eo = get_engagement_opportunity_lookup_from_provider_info(discovery.engagement_opportunity_external_id,
                                                              provider_type, prospect_id)

    eo_id = eo.id

  except ObjectDoesNotExist:

    eo_id = generate_id()

    create_eo = AddEO(eo_id, discovery.engagement_opportunity_external_id,
                      discovery.engagement_opportunity_attrs,
                      provider_type, discovery.provider_action_type, discovery.created_date,
                      profile_id)

    _dispatcher.send_command(prospect_id, create_eo)

  return eo_id


def handle_duplicate_profile(duplicate_prospect_id, existing_external_id, existing_provider_type,
                             _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  existing_profile = get_profile_lookup_from_provider_info(existing_external_id, existing_provider_type)

  existing_prospect_id = existing_profile.prospect_id

  duplicate_prospect_command = MarkProspectAsDuplicate(existing_prospect_id)

  _dispatcher.send_command(duplicate_prospect_id, duplicate_prospect_command)

  return duplicate_prospect_id


def consume_duplicate_prospect(existing_prospect_id, duplicate_prospect_id, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  consume_duplicate_prospect = ConsumeDuplicateProspect(duplicate_prospect_id)

  _dispatcher.send_command(existing_prospect_id, consume_duplicate_prospect)

  return existing_prospect_id


def prospect_is_deleted(prospect_id, _aggregate_repository=None):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  prospect = _aggregate_repository.get(Prospect, prospect_id)

  return prospect.is_deleted
