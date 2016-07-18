import logging
import traceback
from datetime import timedelta

import django_rq
from django_rq.queues import get_failed_queue

MAX_FAILURES = 3
RETRY_DELAYS = 5 * 60

FAILURES_KEY = 'failures'
logger = logging.getLogger(__name__)


# https://gist.github.com/spjwebster/6521272
def retry_handler(job, exc_type, exc_value, traceback):
  job.meta.setdefault(FAILURES_KEY, 0)
  failures_count = job.meta[FAILURES_KEY]
  failures_count += 1

  # Too many failures
  if failures_count >= MAX_FAILURES:
    job.meta[FAILURES_KEY] = failures_count
    job.save()

    logger.warn('job %s: failed too many times times - moving to failed queue' % job.id)

    ret_val = True
  else:
    # Requeue job and stop it from being moved into the failed queue
    scheduler = django_rq.get_scheduler(job.origin)

    scheduled_job = scheduler.enqueue_in(timedelta(seconds=RETRY_DELAYS), job.func, *job.args, **job.kwargs)
    scheduled_job.meta[FAILURES_KEY] = failures_count
    scheduled_job.save()

    # remove the old job from the queue
    job.delete()

    logger.warn('job %s: failed %d times - retrying' % (job.id, failures_count))

    ret_val = False

  return ret_val


# https://github.com/nvie/rq/issues/711
def move_to_failed_queue(job, *exc_info):
  """Default exception handler: move the job to the failed queue."""
  exc_string = ''.join(traceback.format_exception(*exc_info))
  failed_queue = get_failed_queue()
  logger.warning('Moving job to {0!r} queue'.format(failed_queue.name))
  failed_queue.quarantine(job, exc_info=exc_string)
