#!/bin/python3

from __future__ import annotations
import sys
import os
import datetime
import pandas as pd  # type: ignore

from fredapi import Fred  # type: ignore
from dotenv import load_dotenv  # type: ignore

FOLDER = "/home/andy/code/snowflake"

load_dotenv()
args = sys.argv[1:] if len(sys.argv) > 1 else None
fred = Fred(api_key=os.getenv("FRED_API_KEY"))

print(args)

def get_series(series_id, as_of: str | datetime.datetime | None = None) -> pd.Series:
    """Get series by series ID.

    Parameters
    ----------
    series_id : str
        The series ID to get.
    as_of : str | datetime.datetime | None
        The optional date to get the series as of. If a string, it
        must be in the format "YYYY-MM-DD". Defaults to None, which
        gets the most recent data.

    Returns
    -------
    pandas.Series
        The series data.
    """
    if as_of:
        if isinstance(as_of, str):
            as_of = datetime.datetime.strptime(as_of, "%Y-%m-%d")
        out = fred.get_series(series_id, observation_start=as_of)
    out = fred.get_series(series_id)
    out.reset_index().to_parquet(f"{FOLDER}/freddata/{series_id}.parquet", index=False)


def get_series_info(
    series_id: str, attribute: str | None = None
) -> dict[str, str] | str:
    """Get series info by series ID.

    Parameters
    ----------
    series_id : str
        The series ID to get info for.
    attribute : str | None
        The optional attribute to get. If None, returns the entire
        series info. Defaults to None.

    Returns
    -------
    dict[str, str] | str
        The series info. If an attribute is specified, returns the
        value of that attribute.
    """
    return (
        fred.get_series_info(series_id)[attribute]
        if attribute
        else fred.get_series_info(series_id)
    )


def search_series(search_term: str) -> list[dict[str, str]]:
    """Search for series by search term.

    Parameters
    ----------
    search_term : str
        The search term to search for.

    Returns
    -------
    list[dict[str, str]]
        The search results.
    """
    return fred.search(search_term)


def usage_help() -> str:
    """Get help for the script.

    Returns
    -------
    str
        The help text for the script.
    """
    return (
        "Usage:"
        " fred.py search <search_term> "
        "| get <series_id> [as_of] "
        "| info <series_id> [attribute] "
        "| help <function>"
    )


def function_help(function: str) -> str:
    """Get help for a function.

    Parameters
    ----------
    function : str
        The function to get help for.

    Returns
    -------
    str
        The help text for the function.
    """
    return {
        "help": (
            "Get help for a function.\n\n"
            "Parameters\n"
            "----------\n"
            "function : str\n"
            "   The function to get help for.\n\n"
            "Returns\n"
            "-------\n"
            "str\n"
            "   The help text for the function."
        ),
        "search": (
            "Search for series by search term.\n\n"
            "Parameters\n"
            "----------\n"
            "search_term : str\n"
            "   The search term to search for.\n\n"
            "Returns\n"
            "-------\n"
            "list[dict[str, str]]\n"
            "   The search results."
        ),
        "get": (
            "Get series by series ID.\n\n"
            "Parameters\n"
            "----------\n"
            "series_id : str\n"
            "   The series ID to get.\n"
            "as_of : str | datetime.datetime | None\n"
            "   The optional date to get the series as of. If a string, it\n"
            "   must be in the format 'YYYY-MM-DD'. Defaults to None, which\n"
            "   gets the most recent data.\n\n"
            "Returns\n"
            "-------\n"
            "pandas.Series\n"
            "   The series data."
        ),
        "info": (
            "Get series info by series ID.\n\n"
            "Parameters\n"
            "----------\n"
            "series_id : str\n"
            "   The series ID to get info for.\n"
            "attribute : str | None\n"
            "   The optional attribute to get. If None, returns the entire\n"
            "   series info. Defaults to None.\n\n"
            "Returns\n"
            "-------\n"
            "dict[str, str] | str\n"
            "   The series info. If an attribute is specified, returns the\n"
            "   value of that attribute."
        ),
    }[function]


def main():
    if args:
        if args[0] == "search":
            if args[1] == "help":
                print(function_help("search"))
            print(search_series(args[1]))
        elif args[0] == "get":
            if args[1] == "help":
                print(function_help("get"))
            print(get_series(args[1], args[2] if len(args) > 2 else None))
        elif args[0] == "info":
            if args[1] == "help":
                print(function_help("info"))
            print(get_series_info(args[1], args[2] if len(args) > 2 else None))
        elif args[0] == "help":
            if len(args) > 1:
                print(function_help(args[1]))
            else:
                print(usage_help())

    else:
        print(usage_help())


if __name__ == "__main__":
    out = main()

    if out:
        if isinstance(out, pd.Series):
            out.reset_index().to_parquet(f"./freddata/{args[1]}.parquet", index=False)
        elif isinstance(out, dict):
            print(out)
        elif isinstance(out, pd.DataFrame):
            out.to_parquet(f"./freddata/{args[1]}.parquet", index=False)
        else:
            print(out)

