import os
import hashlib
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from apps.heritage.models import HeritageSite
from apps.festivals.models import Festival
from apps.arts.models import ArtForm
from apps.cuisine.models import CuisineDish
from apps.stories.models import Story

class Command(BaseCommand):
    help = "Validates that all cultural items have unique, existing image files and valid credits."

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed verification for each item.',
        )

    def handle(self, *args, **options):
        verbose = options.get('verbose', False)
        errors = []
        
        # Models to check
        categories = [
            ("Heritage Site", HeritageSite.objects.all(), "hero_image"),
            ("Festival", Festival.objects.all(), "hero_image"),
            ("Art Form", ArtForm.objects.all(), "hero_image"),
            ("Cuisine Dish", CuisineDish.objects.all(), "hero_image"),
            ("Cultural Story", Story.objects.all(), "cover_image"),
        ]

        seen_files = {}   # rel_path -> item_repr
        seen_hashes = {}  # file_hash -> item_repr
        total_checked = 0

        static_root = Path(settings.BASE_DIR) / 'static'

        for cat_name, qs, img_attr in categories:
            for item in qs:
                total_checked += 1
                item_name = getattr(item, 'name', None) or getattr(item, 'title', None) or str(item)
                item_id = f"[{cat_name}] {item_name} (slug: {item.slug})"
                img_val = getattr(item, img_attr, None)

                # 1. Missing image field value
                if not img_val:
                    errors.append(f"(b) Missing image URL/path on {item_id}")
                    continue

                # Clean static path
                img_clean = str(img_val).strip()
                if img_clean.startswith('/static/'):
                    rel_path = img_clean[len('/static/'):]
                elif img_clean.startswith('static/'):
                    rel_path = img_clean[len('static/'):]
                else:
                    rel_path = img_clean.lstrip('/')

                disk_path = static_root / rel_path

                # 2. Condition (b): Any image file is missing
                if not disk_path.exists() or not disk_path.is_file():
                    errors.append(f"(b) Missing image file on disk: '{disk_path}' for {item_id}")
                    continue

                is_placeholder = disk_path.suffix.lower() == '.svg' or 'placeholder' in disk_path.name.lower()

                # 3. Condition (c): Any credit field is empty for a real photo
                if not is_placeholder:
                    credit = getattr(item, 'image_credit', '') or ''
                    source_url = getattr(item, 'image_source_url', '') or ''
                    license_name = getattr(item, 'image_license', '') or ''

                    missing_credits = []
                    if not credit.strip():
                        missing_credits.append('image_credit')
                    if not source_url.strip():
                        missing_credits.append('image_source_url')
                    if not license_name.strip():
                        missing_credits.append('image_license')

                    if missing_credits:
                        errors.append(
                            f"(c) Empty credit field(s) {missing_credits} for real photo on {item_id}"
                        )

                # 4. Condition (a): Shared image file or identical file hash
                # Read and hash file content
                try:
                    with open(disk_path, 'rb') as f:
                        file_bytes = f.read()
                    file_hash = hashlib.sha256(file_bytes).hexdigest()
                except Exception as e:
                    errors.append(f"Could not read image file '{disk_path}' for {item_id}: {e}")
                    continue

                # Placeholder files are allowed to be reused; real photos MUST be distinct
                if not is_placeholder:
                    norm_path = str(rel_path).replace('\\', '/').lower()
                    if norm_path in seen_files:
                        errors.append(
                            f"(a) Shared image file: '{norm_path}' is used by both {item_id} and {seen_files[norm_path]}"
                        )
                    else:
                        seen_files[norm_path] = item_id

                    if file_hash in seen_hashes:
                        errors.append(
                            f"(a) Identical file content hash ({file_hash[:12]}...) shared between {item_id} and {seen_hashes[file_hash]}"
                        )
                    else:
                        seen_hashes[file_hash] = item_id

                if verbose:
                    self.stdout.write(f"Verified {item_id} -> {rel_path} (hash: {file_hash[:8]}...)")

        if errors:
            self.stderr.write(self.style.ERROR(f"\n[FAIL] check_images failed with {len(errors)} error(s):"))
            for err in errors:
                self.stderr.write(self.style.ERROR(f"  * {err}"))
            raise CommandError(f"Image validation check failed with {len(errors)} errors.")

        self.stdout.write(
            self.style.SUCCESS(
                f"\n[OK] check_images passed: {total_checked} items verified. "
                f"All real photos have unique files, distinct hashes, and complete credit/license metadata."
            )
        )
