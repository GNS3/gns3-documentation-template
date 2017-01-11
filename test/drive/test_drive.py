import os
import lxml
import json
from unittest.mock import MagicMock

from drive import Drive
from drive.document import DriveDocument


def test_copy_ressources(tmpdir):
    d = Drive()
    d._copy_ressources(str(tmpdir))
    assert (tmpdir / 'ressources').exists()
    assert (tmpdir / 'ressources' / 'style.css').exists()


def test_permissions_for_anyone():
    d = Drive()
    d._service = MagicMock()
    assert d._permissions_for_anyone({"permissions": [
        {
            'role': 'owner',
            'type': 'user'
        },
        {
            'role': 'writer',
            'type': 'user'
        },
        {
            'domain': 'example.org',
            'role': 'writer',
            'allowFileDiscovery': False,
            'type': 'domain'
        },
        {
            'role': 'commenter',
            'type': 'anyone',
        }
    ]})
    assert d._permissions_for_anyone({"permissions": [
        {
            'role': 'owner',
            'type': 'user'
        }
    ]}) is False
