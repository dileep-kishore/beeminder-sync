"""
    Tests for the query function
"""

import pytest

from beeminder_sync.query import query


@pytest.mark.usefixtures("github_json")
class TestQuery:
    """ Tests for the query function """

    def test_query(self, github_json):
        query_string1 = ".[0] | {message: .commit.message, name: .commit.committer.name}"
        data1 = query(github_json, query_string1)
        assert isinstance(data1[''], list)
        assert len(data1) == 1
        query_string2 = ".[] | {message: .commit.message, name: .commit.committer.name}"
        data2 = query(github_json, query_string2)
        assert isinstance(data2[''], list)
        assert len(data2['']) > 1
