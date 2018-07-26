"""
    Tests for the BeeSync class
"""


import pytest

from beeminder_sync import BeeSync


@pytest.mark.usefixtures("config_paths")
class TestBeeminderSync:
    """ Tests for the BeeSync class """

    def test_init(self, config_paths):
        bee_sync = BeeSync(*config_paths, spinner=False)
        assert bee_sync.base_dir == config_paths[0]
        assert bee_sync.config_path == config_paths[1]
        assert "beeminder" in bee_sync.config.sections()
        options = bee_sync.config.options("beeminder")
        assert all(x in options for x in ["api", "username", "auth_token"])

    def test_update_get(self, config_paths):
        bee_sync = BeeSync(*config_paths, spinner=False)
        bee_sync.update("beeminder", "username", "tester")
        assert bee_sync.get("beeminder", "username") == "tester"
        bee_sync.update("beeminder", "auth_token", "token")
        assert bee_sync.get("beeminder", "auth_token") == "token"
