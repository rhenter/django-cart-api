import random

from django.conf import settings


class MasterReplicaRouter:
    route_app_labels = {'auth', 'contenttypes', 'user', 'sessions'}
    read_write_models = {'targetcol', 'sectionsetup', 'taskresult', 'periodictask'}
    databases_keys = settings.DATABASES.keys()
    replica_databases = settings.REPLICA_DATABASES
    has_collector_database = 'collector' in databases_keys

    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        if model._meta.app_label == 'collector' and self.has_collector_database:
            return 'collector'

        read_write_conditions = (
           not self.replica_databases,
           model._meta.app_label in self.route_app_labels,
           model._meta.model_name in self.read_write_models,
        )
        if any(read_write_conditions) or not self.replica_databases:
            return 'default'
        return random.choice(self.replica_databases)

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        if model._meta.app_label == 'collector' and self.has_collector_database:
            return 'collector'

        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True
