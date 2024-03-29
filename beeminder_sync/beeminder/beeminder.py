"""
    Module to interact with the beeminder api
"""

import maya
import sys
from typing import Any, Dict, List, Union
import requests

from furl import furl
from halo import Halo

from beeminder_sync.logger import log
from ..beeminder_sync import BeeSync
from ..query import query
from ..output import output


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
        spinner : bool, optional
            If True then `Halo` spinners are enabled
            Default value is True

        Attributes
        ----------
        goals : List[str]
            List of `beeminder` goals
        goal_data : Dict[str, dict]
            Data for all goals
    """

    def __init__(self, base_url: str, user_name: str, auth_token: str, spinner: bool = True) -> None:
        self._spinner = Halo(
            text="Connecting to the Beeminder api...",
            color="blue",
            spinner="dots",
            enabled=spinner
        )
        self._spinner.start()
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
        elif endpoint in {'goals', 'datapoints'}:
            url.add(path=f"users/{self._user_name}/goals/")
        else:
            raise TypeError("The endpoint you entered is not supported")
        url.add(args={"auth_token": self._auth_token})
        return url

    @property
    def user_details(self) -> Dict[str, Any]:
        """
            Get user details

            Returns
            -------
            Dict[str, Any]
        """
        data = {i: self._user_resource[i] for i in ["username", "timezone", "subscription", "updated_at", "id"]}
        return {"user": data}

    # TODO: Incorporate `diff_since` in the call
    def _get_goals(self) -> List[str]:
        """
            Get all the `beeminder` goals for the current user

            Returns
            -------
            List[str]
                A list of goals in the current user's `beeminder` profile
        """
        self._spinner.text = "Getting goal list..."
        self._spinner.start()
        user_url = self._url_maker('user')
        response = requests.get(user_url)
        log.info(f"Attempting to connect to {user_url}")
        response.raise_for_status()
        log.info("Connection successful. Getting list of goals")
        response_data = response.json()
        self._user_resource = response_data
        self._spinner.succeed("Goal list retrieved succesfully")
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
        log.info(f"Attempting to connect to {goal_url}")
        response.raise_for_status()
        log.info(f"Connection successful. Retrieving data for {goal}")
        return {"goal": response.json()}

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
        self._spinner.text = "Retrieving datapoints..."
        self._spinner.start()
        data_url = self._url_maker('datapoints')
        data_url.add(path=f"{goal}/datapoints.json")
        response = requests.get(data_url)
        log.info(f"Attempting to connect to {data_url}")
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise ValueError(f"Goal {goal} not found. The following goals were found: {self.goals}")
        log.info(f"Connection successful. Retrieving data-points for {goal}")
        self._spinner.succeed(f"Data for {goal} retrieved successfully")
        return {"datapoints": response.json()}

    def create_datapoint(
            self,
            goal: str,
            value: int,
            comment: str = '',
            timestamp: Union[int, float] = maya.now().epoch
    ) -> bool:
        """
            Create datapoint for a particular goal

            Parameters
            ----------
            goal : str
                The goal for which datapoint needs to be created
            value : int
                The value for the new datapoint
            timestamp : Union[int, float]
                Timestamp for the new datatpoint (default is current time)
            comment : str
                Comment for the new datapoint (default is '')
        """
        self._spinner.text = "Creating datapoints..."
        self._spinner.start()
        data_url = self._url_maker('datapoints')
        data_url.add(path=f"{goal}/datapoints.json")
        if isinstance(timestamp, str):
            try:
                timestamp = maya.parse(timestamp).epoch
            except:
                self._spinner.fail(f"Invalid date string: {timestamp}")
                sys.exit()
        data_url.add(args={
            'value': value,
            'timestamp': timestamp,
            'comment': comment
        })
        response = requests.post(data_url)
        log.info(f"Attempting to connect to {data_url}")
        response.raise_for_status()
        log.info(f"Connection successful. Creating data-point for {goal}")
        self._spinner.succeed("Creation successful")
        return {"datapoints": response.json()}

    @classmethod
    def from_config(cls, beesync: BeeSync) -> "Beeminder":
        """
            Create `Beeminder` instance using configuration stored in `BeeSync` object

            Parameters
            ----------
            beesync : BeeSync
                The `BeeSync` object storing the configuration

            Returns
            -------
            Beeminder
        """
        base_url = beesync.get('beeminder', 'api', silent=True)
        user_name = beesync.get('beeminder', 'username', silent=True)
        auth_token = beesync.get('beeminder', 'auth_token', silent=True)
        return cls(base_url, user_name, auth_token)

    def set_spinner(self, settings: Dict[str, str]) -> Halo:
        """
            Update settings for spinner instance

            Parameters
            ----------
            settings : Dict[str, str]
                A dictionary containing the updated settings for the spinner

            Returns
            -------
            Halo
                Returns the spinner instance
        """
        for key in settings:
            if key in ['spinner', 'text', 'color']:
                setattr(self._spinner, key, settings[key])
            else:
                raise KeyError("Unsupported attribute supplied to spinner instance")
        return self._spinner

    def fail(self, text: str) -> None:
        """
            Creates a failure message using the `Halo` spinner object

            Parameters
            ----------
            text : str

            Returns
            -------
            None
        """
        self._spinner.fail(text)

    @staticmethod
    def query(response: dict, query_string: str) -> dict:
        """
            Query beeminder api response using query_string

            Parameters
            ----------
            response : dict
                Beeminder api response to query
            query_string : str
                `jq` compatible query string

            Returns
            -------
            dict
        """
        return query(response, query_string)

    @staticmethod
    def output(response: dict, format: str) -> str:
        """
            Format beeminder api response

            Parameters
            ----------
            response : dict
                Beeminder api response to format
            format : {'json', 'table'}
                Output format

            Returns
            -------
            str
        """
        return output(response, format)
