from django.db import migrations


class Migration(migrations.Migration):
    """
    Initial migration to enable the pgvector and pg_stat_statements extensions using raw SQL.

    WARNING: This uses 'CREATE EXTENSION ...;' directly without 'IF NOT EXISTS'.
    It will FAIL if either extension already exists in the target database.
    Consider using CreateExtension operation or 'IF NOT EXISTS' for safety.
    """

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            sql='CREATE EXTENSION IF NOT EXISTS vector;',
            reverse_sql='DROP EXTENSION IF EXISTS vector;',
        ),
        migrations.RunSQL(
            sql='CREATE EXTENSION IF NOT EXISTS pg_stat_statements;',
            reverse_sql='DROP EXTENSION IF EXISTS pg_stat_statements;',
        ),
    ]
