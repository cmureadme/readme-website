import time

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand

temp_storage = FileSystemStorage(location=settings.TEMP_UPLOAD_ROOT)
MAX_AGE_SECONDS = 60 * 60 * 24  # 24 hours


class Command(BaseCommand):
    help = "Deletes stale temp file uploads from the Issue upload form."

    def handle(self, *args, **kwargs):
        if not temp_storage.exists("."):
            self.stdout.write("No temp upload directory found — nothing to clean.")
            return

        cutoff = time.time() - MAX_AGE_SECONDS
        _, files = temp_storage.listdir(".")

        deleted = 0
        for name in files:
            modified = temp_storage.get_modified_time(name).timestamp()
            if modified < cutoff:
                temp_storage.delete(name)
                deleted += 1

        self.stdout.write(f"Deleted {deleted} stale temp upload(s).")
