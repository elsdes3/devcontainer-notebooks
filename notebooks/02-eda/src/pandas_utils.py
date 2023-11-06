#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Pandas DataFrame utilities."""


import pandas as pd
from IPython.display import display

# pylint: disable=invalid-name,abstract-class-instantiated


def convert_dtypes_auto(df: pd.DataFrame) -> pd.DataFrame:
    """Convert datatypes of DataFrame columns."""
    df = df.convert_dtypes(
        convert_integer=True,
        convert_string=True,
        convert_floating=True,
        convert_boolean=True,
    )
    return df


def show_df(df: pd.DataFrame) -> None:
    """Show datatypes and number of missing values in column headers."""
    df = df.copy()
    df.columns = pd.MultiIndex.from_tuples(
        tuples=list(zip(df.columns, df.dtypes, df.isna().sum())),
        names=["column", "dtype", "missing"],
    )
    display(df)
