from hashlib import sha256
from pathlib import Path

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


def create_dir_if_not_exists(path: Path):
    if not path.exists():
        path.mkdir(parents=True)


def get_sha256_hash(byte_content: bytes):
    return sha256(byte_content).hexdigest()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

