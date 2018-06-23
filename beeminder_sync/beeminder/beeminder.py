"""
    Module to interact with the beeminder api
"""

import json
from typing import Any, Dict, List
import requests


class Beeminder:
    """
        Interface to the `beeminder` api

        Parameters
        ----------
        base_url : str
            The base url of the `beeminder` api
        user_name : str
            `beeminder` username
        auth_token : str
            `beeminder` authentication token

        Attributes
        ----------
        goals : List[str]
            List of `beeminder` goals
        goal_data : Dict[str, dict]
            Data for all goals
    """

    def __init__(self, base_url: str, user_name: str, auth_token: str) -> None:
        self._base_url = base_url
        self._user_name = user_name
        self._auth_token = auth_token
        goals_url = f"{base_url}/{user_name}/goals?auth_token={auth_token}"
        self.goals = self._get_goals(goals_url)
        return None

    @staticmethod
    def _get_goals(goals_url: str) -> List[str]:
        """
            Get all the `beeminder` goals for the current user

        Parameters
        ----------
        goals_url : str

        Returns
        -------
        List[str]
            A list of goals in the current user's `beeminder` profile
        """
        response = requests.get(goals_url)
        response_data = json.loads(response.text)
        return [elem['slug'] for elem in response_data]

    def __getitem__(self, goal: str) -> Dict[str, Any]:
        """
        """
        pass

    @property
    def goal_data(self) -> Dict[str, dict]:
        """
        """
        pass
