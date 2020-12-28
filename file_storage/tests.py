from pathlib import Path

from django.test import TestCase

# Create your tests here.
from file_storage.utils import create_dir_if_not_exists, get_sha256_hash


def test_create_dir_if_not_exists():
    path = Path('/tmp/somepath')
    create_dir_if_not_exists(path)
    assert path.exists(), 'Something went wrong while dir creating'
    path.rmdir()


def test_get_sha256_hash():
    assert get_sha256_hash('Some string'.encode()) == '2beaf0548e770c4c392196e0ec8e7d6d81cc9280ac9c7f3323e4c6abc231e95a'