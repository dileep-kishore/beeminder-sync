"""
    Tests for the beeminder api
"""

import requests
import pytest
from furl import furl
from beeminder_sync.beeminder import Beeminder


@pytest.mark.usefixtures("beeminder_config")
class TestBeeminderApi:

    """ Tests for the beeminder api """

    def test_config(self, beeminder_config):
        for req_field in beeminder_config['required_fields']:
            assert req_field in beeminder_config.keys(), \
                "Beeminder configuration missing required field"
            assert beeminder_config[req_field], \
                "Beeminder configuration has empty value in required field"

    def test_credentials(self, beeminder_config):
        base_url = beeminder_config['api']
        username = beeminder_config['username']
        auth_token = beeminder_config['auth_token']
        user_url = furl(base_url)
        user_url.add(path=f"users/{username}.json")
        user_url.add(args={"auth_token": auth_token})
        response = requests.get(user_url)
        assert response.status_code != 404
        response_data = response.json()
        assert response_data['username'] == username

    def test_interface(self, beeminder_config):
        base_url = beeminder_config['api']
        username = beeminder_config['username']
        auth_token = beeminder_config['auth_token']
        Beeminder(base_url, username, auth_token)
        assert True
        with pytest.raises(requests.exceptions.HTTPError):
            Beeminder(base_url, 'test', 'token')
