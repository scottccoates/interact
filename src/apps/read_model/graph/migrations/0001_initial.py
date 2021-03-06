# encoding: utf8
from django.db import migrations

from src.libs.graphdb_utils.services import graphdb_provider


def add_neo_index(models, schema_editor):
  graph_db = graphdb_provider.get_graph_client()
  graph_db.query("CREATE CONSTRAINT ON (client_id:Client) ASSERT client_id.id IS UNIQUE")
  graph_db.query("CREATE CONSTRAINT ON (topic:Topic) ASSERT topic.id IS UNIQUE")
  graph_db.query("CREATE CONSTRAINT ON (ea:EngagementAssignment) ASSERT ea.id IS UNIQUE")
  graph_db.query("CREATE CONSTRAINT ON (eo:EngagementOpportunity) ASSERT eo.id IS UNIQUE")
  graph_db.query("CREATE CONSTRAINT ON (profile:Profile) ASSERT profile.id IS UNIQUE")
  graph_db.query("CREATE CONSTRAINT ON (prospect:Prospect) ASSERT prospect.id IS UNIQUE")


def drop_neo_index(models, schema_editor):
  graph_db = graphdb_provider.get_graph_client()
  graph_db.query("DROP CONSTRAINT ON (client_id:Client) ASSERT client_id.id IS UNIQUE")
  graph_db.query("DROP CONSTRAINT ON (topic:Topic) ASSERT topic.id IS UNIQUE")
  graph_db.query("DROP CONSTRAINT ON (ea:EngagementAssignment) ASSERT ea.id IS UNIQUE")
  graph_db.query("DROP CONSTRAINT ON (eo:EngagementOpportunity) ASSERT eo.id IS UNIQUE")
  graph_db.query("DROP CONSTRAINT ON (profile:Profile) ASSERT profile.id IS UNIQUE")
  graph_db.query("DROP CONSTRAINT ON (prospect:Prospect) ASSERT prospect.id IS UNIQUE")


class Migration(migrations.Migration):
  dependencies = [
    ('common_domain', '0001_initial'),
  ]

  operations = [
    migrations.RunPython(add_neo_index, drop_neo_index),
  ]
