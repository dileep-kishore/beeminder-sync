"""
    Module to interact with the beeminder api
"""

from time import time
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

    def _url_maker(self, endpoint: str) -> furl:
        """
            Create urls based on endpoint

            Parameters
            ----------
            endpoint : str
                The url endpoint to be queried

            Returns
            -------
            furl
                A `furl` instance of the url
        """
        url = furl(self._base_url)
        if endpoint == 'user':
            url.add(path=f"users/{self._user_name}.json")
        elif endpoint in ['goals', 'datapoints']:
            url.add(path=f"users/{self._user_name}/goals/")
        else:
            raise TypeError("The endpoint you entered is not supported")
        url.add(args={"auth_token": self._auth_token})
        return url

    # TODO: Incorporate `diff_since` in the call
    def _get_goals(self) -> List[str]:
        """
            Get all the `beeminder` goals for the current user

            Returns
            -------
            List[str]
                A list of goals in the current user's `beeminder` profile
        """
        user_url = self._url_maker('user')
        response = requests.get(user_url)
        response.raise_for_status()
        response_data = response.json()
        self._user_resource = response_data
        return response_data['goals']

    def __getitem__(self, goal: str) -> Dict[str, Any]:
        """
            Retrieve information for a particular goal

            Parameters
            ----------
            goal : str
                The goal to be queried

            Returns
            -------
            Dict[str, Any]
                A dictionary containing all the goal related data
        """
        if goal not in self.goals:
            raise KeyError(f"{goal} not found in user's beeminder goals")
        goal_url = self._url_maker('goals')
        goal_url.add(path=f"{goal}.json")
        response = requests.get(goal_url)
        response.raise_for_status()
        return response.json()

    def get_datapoints(self, goal: str) -> List[Dict[str, Any]]:
        """
            Retrieve datapoints for a particular goal

            Parameters
            ----------
            goal : str
                The goal to be queried

            Returns
            -------
            List[Dict[str, Any]]
                A list of every datapoint entry for the goal
        """
        data_url = self._url_maker('datapoints')
        data_url.add(path=f"{goal}/datapoints.json")
        response = requests.get(data_url)
        response.raise_for_status()
        return response.json()

    def create_datapoint(self, goal: str, value: int, timestamp: float = time(),
                         comment: str = '') -> bool:
        """
            Create datapoint for a particular goal

            Parameters
            ----------
            goal : str
                The goal for which datapoint needs to be created
            value : int
                The value for the new datapoint
            timestamp : float
                Timestamp for the new datatpoint (default is current time)
            comment : str
                Comment for the new datapoint (default is '')
        """
        data_url = self._url_maker('datapoints')
        data_url.add(path=f"{goal}/datapoints.json")
        data_url.add(args={
            'value': value,
            'timestamp': timestamp,
            'comment': comment
        })
        response = requests.post(data_url)
        response.raise_for_status()
        return response.json()
