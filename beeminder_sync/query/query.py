"""
    Module that contains functions to help query API JSON dumps
"""

import pyjq


def query(response: dict, query_string: str) -> list:
    """
        Get subset of response dictionary using the query string
        The format for the 'query_string' is identical to `jq`

        Parameters
        ----------
        response : dict
            The output of the beeminder subcommand
        query_string : str
            String to query the response
            Eg. '.datapoints[] | {comment, timestamp}'

        Returns
        -------
        dict
            The parsed dictionary

        Refer
        -----
        `jq` is a lightweight and flexible command-line JSON processor
        refer: https://stedolan.github.io/jq/
    """
    return pyjq.all(query_string, response)
