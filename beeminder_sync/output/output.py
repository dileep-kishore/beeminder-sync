"""
    Module that contains functions to format API JSON dumps
"""

import json


def json_output(response: dict) -> str:
    """
        Output API response in prettified JSON format

        Parameters
        ----------
        response : dict

        Returns
        -------
        str
    """
    return json.dumps(response, indent=2, sort_keys=True)


def table_output(response: dict) -> str:
    """
        Output API response in prettified Table format

        Parameters
        ----------
        response : dict

        Returns
        -------
        str
    """
    # TODO: How to find screen width
    raise NotImplementedError


def output(response: dict, format: str = "json") -> str:
    """
        Output API response in requested format

        Parameters
        ----------
        response : dict
            The API response JSON
        format : {'json', 'table'}, optional
            The format to convert the API response into
            Default value is 'json'

        Returns
        -------
        str
            The API response in the requested format
    """
    if format == "json":
        return json_output(response)
    if format == "table":
        return table_output(response)
    raise ValueError("Supported formats are 'json' and 'table'")
