from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from magazine.models import Author


class Command(BaseCommand):
    help = "Rename author images and remove unused ones. Use --dry-run to test"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would happen without making changes.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        storage = Author._meta.get_field("img").storage

        used_files = set()

        for author in Author.objects.exclude(img__isnull=True).exclude(img=""):
            old_name = author.img.name
            ext = Path(old_name).suffix.lower()
            new_name = f"author_images/{author.slug}{ext}"


            if old_name != new_name:
                if not storage.exists(old_name):
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipping missing file: {old_name}"
                        )
                    )
                    continue

                if dry_run:
                    self.stdout.write(
                        f"[RENAME] {old_name} -> {new_name}"
                    )
                else:
                    self.stdout.write(
                        f"Renaming {old_name} -> {new_name}"
                    )

                    with storage.open(old_name, "rb") as f:
                        storage.save(new_name, ContentFile(f.read()))

                    storage.delete(old_name)

                    author.img.name = new_name
                    author.save(update_fields=["img"])

            if storage.exists(new_name):
                used_files.add(new_name)

        # Find unused images
        _, files = storage.listdir("author_images")

        for file in files:
            path = f"author_images/{file}"

            if path not in used_files:
                if dry_run:
                    self.stdout.write(f"[DELETE] {path}")
                else:
                    self.stdout.write(f"Deleting {path}")
                    storage.delete(path)

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "Dry run complete. No files were changed."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "Author images fixed successfully."
                )
            )