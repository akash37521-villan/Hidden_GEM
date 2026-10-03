import time
import logging
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Management command: python manage.py wait_for_db

    Polls the default database connection until it is available.
    Used inside the Docker entrypoint so the web container doesn't
    start before PostGIS is ready to accept connections.
    """

    help = "Waits for the database to be available before proceeding."

    def add_arguments(self, parser):
        parser.add_argument(
            "--max-retries",
            type=int,
            default=30,
            help="Maximum number of connection attempts (default: 30).",
        )
        parser.add_argument(
            "--sleep",
            type=float,
            default=2.0,
            help="Seconds to wait between retries (default: 2).",
        )

    def handle(self, *args, **options):
        max_retries = options["max_retries"]
        sleep_seconds = options["sleep"]

        self.stdout.write("Waiting for database...")
        for attempt in range(1, max_retries + 1):
            try:
                conn = connections["default"]
                conn.ensure_connection()
                self.stdout.write(self.style.SUCCESS("Database available!"))
                return
            except OperationalError:
                self.stdout.write(
                    f"  Attempt {attempt}/{max_retries} — DB unavailable, "
                    f"retrying in {sleep_seconds}s..."
                )
                time.sleep(sleep_seconds)

        self.stderr.write(
            self.style.ERROR(
                f"Database not available after {max_retries} attempts. Exiting."
            )
        )
        raise SystemExit(1)
