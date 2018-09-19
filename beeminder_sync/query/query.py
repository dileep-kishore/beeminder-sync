"""
    Module that contains functions to help query API JSON dumps
"""

import pyjq


def query(response: dict, query_string: str) -> dict:
    """
        Get subset of response dictionary using the query string
        The format for the 'query_string' is identical to `jq`

        Parameters
        ----------
        response : dict
            The API response JSON
        query_string : str
            String to query the response
            Eg. '.datapoints[] | {comment, timestamp}'

        Returns
        -------
        dict
            The parsed dictionary

        Notes
        -----
        `jq` is a lightweight and flexible command-line JSON processor
        refer: https://stedolan.github.io/jq/
    """
    key = query_string.split('|')[0].strip().split('[')[0].strip('.')
    result = pyjq.all(query_string, response)
    if len(result) == 1 and isinstance(result[0], list):
        result = result[0]
    return {key: result}
