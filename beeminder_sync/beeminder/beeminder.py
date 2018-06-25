"""
    Module to interact with the beeminder api
"""

from typing import Any, Dict, List
import requests
from furl import furl


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
        self.goals = self._get_goals()
        return None

    # TODO: Incorporate `diff_since` in the call
    def _get_goals(self) -> List[str]:
        """
            Get all the `beeminder` goals for the current user

            Returns
            -------
            List[str]
                A list of goals in the current user's `beeminder` profile
        """
        goals_url = furl(self._base_url)
        goals_url.add(path=f"users/{self._user_name}.json")
        goals_url.add(args={"auth_token": self._auth_token})
        response = requests.get(goals_url)
        response.raise_for_status()
        response_data = response.json()
        self._user_resource = response_data
        return response_data['goals']

    def __getitem__(self, goal: str) -> Dict[str, Any]:
        """
            Retrieve information about a particular goals

            Returns
            -------
            Dict[str, Any]
                A dictionary containing all the goal related data
        """
        goal_url = furl(self._base_url)
        goal_url.add(path=f"users/{self._user_name}/goals/{goal}.json")
        goal_url.add(args={"auth_token": self._auth_token})
        response = requests.get(goal_url)
        response.raise_for_status()
        return response.json()
