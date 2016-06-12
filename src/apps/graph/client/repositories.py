from neo4jrestclient.client import Node, Relationship

from src.domain.common import constants
from src.libs.graphdb_utils.services import graphdb_provider


def write_client_to_graphdb(client_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      MERGE (n:Client {id: {client_id}})
      RETURN n
  '''

  params = {
    'client_id': client_id,
  }

  ret_val = gdb.query(q, params=params, returns=(Node,))
  return ret_val[0][0]


def write_ta_topic_to_graphdb(client_id, ta_topic_id, topic_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
    MATCH (client:Client), (topic:Topic)
    WHERE client.id = { client_id }
    AND topic.id = { topic_id }
    MERGE (client)-[r:TA_TOPIC]->(topic)
    SET r.id = { ta_topic_id }
    RETURN r
  '''

  ta_topic_id = ta_topic_id
  topic_id = topic_id
  params = {

    'client_id': client_id,
    'ta_topic_id': ta_topic_id,
    'topic_id': topic_id,

  }

  ret_val = gdb.query(q, params=params, returns=(Relationship,))

  return ret_val[0][0]


def write_ea_to_graphdb(id, attrs, client_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      MERGE (ea:EngagementAssignment {id: {engagement_assignment_id}})
      MATCH (client:Client {id: {client_id}})
      MERGE (client)-[:HAS_ASSIGNMENT]->(ea)
  '''

  params = {
    'engagement_assignment_id': id,
    'client_id': client_id,
  }

  if constants.EO_IDS in attrs:
    q += '''
        FOREACH (eo IN { eos } |
          MATCH (eo:EngagementOpportunity {id: eo.id})
          MERGE (eo)-[:ASSIGNED_TO]->(ea))
    '''

  q += '''
    RETURN ea
  '''

  params['eos'] = [{'id': eo_id} for eo_id in attrs[constants.EO_IDS]]

  ret_val = gdb.query(q, params=params, returns=(Node,))
  return ret_val[0][0]
