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
    width = 120
    # NOTE: We assume that results are a flat list of dictionaries inside an object
    header = list(response.keys())[0]
    rows = list(response[header])
    # NOTE: We assume that all items in list have the same number of keys
    cols = list(rows[0].keys())
    table = ['-' * width]
    table.append("|{content:^{width}}|".format(content=header, width=width - 2))
    table.append('-' * width)
    col_width = width // len(cols)
    col_headers = []
    for col in cols:
        col_headers.append("|{content:^{width}}|".format(content=col, width=col_width - 2))
    table.append(''.join(col_headers))
    table.append('-' * width)
    for row in rows:
        row_data = [''] * len(row)
        for key, value in row.items():
            ind = cols.index(key)
            row_data[ind] = "|{content:^{width}}|".format(content=value, width=col_width - 2)
        table.append(''.join(row_data))
    return '\n'.join(table)


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
