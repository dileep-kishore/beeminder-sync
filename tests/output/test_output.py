"""
    Tests for the output functions
"""

import pytest

from beeminder_sync.output import json_output, table_output


@pytest.mark.usefixtures("github_json", "beeminder_interface")
class TestOutput:
    """ Tests for the output functions """

    def test_json_output(self, github_json):
        assert json_output({"github": github_json})

    def test_table_output(self, beeminder_interface):
        response = beeminder_interface.get_datapoints("test_goal")
        assert table_output(response)
