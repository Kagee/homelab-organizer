from django.db.backends.sqlite3 import base

# https://blog.pecar.me/django-sqlite-benchmark
# https://blog.pecar.me/django-sqlite-dblock


class DatabaseWrapper(base.DatabaseWrapper):
    def _start_transaction_under_autocommit(self):
        # Acquire a write lock immediately for transactions
        self.cursor().execute("BEGIN IMMEDIATE")
