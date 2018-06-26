"""
    Tests for the beeminder api
"""

import random
import requests
import pytest
from furl import furl
from beeminder_sync.beeminder import Beeminder


@pytest.mark.usefixtures("beeminder_config")
class TestBeeminderApi:

    """ Tests for the beeminder api """

    def test_config(self, beeminder_config):
        """ Test for correct configuration settings """
        for req_field in beeminder_config['required_fields']:
            assert req_field in beeminder_config.keys(), \
                "Beeminder configuration missing required field"
            assert beeminder_config[req_field], \
                "Beeminder configuration has empty value in required field"

    def test_credentials(self, beeminder_config):
        """ Test for correct credentials in `config.json` """
        base_url = beeminder_config["api"]
        username = beeminder_config["username"]
        auth_token = beeminder_config["auth_token"]
        user_url = furl(base_url)
        user_url.add(path=f"users/{username}.json")
        user_url.add(args={"auth_token": auth_token})
        response = requests.get(user_url)
        assert response.status_code != 404
        response_data = response.json()
        assert response_data["username"] == username

    def test_interface(self, beeminder_config):
        """ Test whether the `Beeminder` interface connects to the api """
        base_url = beeminder_config["api"]
        username = beeminder_config["username"]
        auth_token = beeminder_config["auth_token"]
        Beeminder(base_url, username, auth_token)
        with pytest.raises(requests.exceptions.HTTPError):
            Beeminder(base_url, "test", "token")

    def test_getitem(self, beeminder_config):
        """ Test whether the `Beeminder` interface gets goal data """
        base_url = beeminder_config["api"]
        username = beeminder_config["username"]
        auth_token = beeminder_config["auth_token"]
        interface = Beeminder(base_url, username, auth_token)
        goal = random.choice(interface.goals)
        goal_data = interface[goal]
        assert goal_data["slug"] == goal

    def test_get_datapoints(self, beeminder_interface):
        goal = random.choice(beeminder_interface.goals)
        datapoints = beeminder_interface.get_datapoints(goal)
        assert len(datapoints) >= 1
