import pytest
import polars as pl
from pytest_lazy_fixtures import lf as lazy_fixture
from {{ cookiecutter.project_slug }}.utils.numerical import (
    parse_european_decimal_columns,
)


"""
Tests for the `parse_european_decimal_columns` function.

These tests ensure that:
- simple European decimal strings are correctly parsed
- multiple columns with European decimal strings are correctly parsed
- columns with None values are correctly handled
- wrong column names raise appropriate errors
- invalid European decimal strings raise appropriate errors
"""


@pytest.mark.parametrize(
    argnames="df",
    argvalues=[lazy_fixture("df_european_decimal_simple")],
)
def test_parse_european_decimal_columns_simple(df):
    result = parse_european_decimal_columns(df, {"price": pl.Float32()})
    assert result["price"].to_list() == pytest.approx([1.23, 4.56], rel=1e-6)


@pytest.mark.parametrize(
    argnames="df",
    argvalues=[lazy_fixture("df_european_decimal_multi")],
)
def test_parse_european_decimal_columns_multi(df):
    result = parse_european_decimal_columns(
        df,
        {
            "price": pl.Float64,
            "tax": pl.Float64,
        },
    )
    assert result.row(0) == pytest.approx((1.23, 0.20), rel=1e-6)


@pytest.mark.parametrize(
    argnames="df",
    argvalues=[lazy_fixture("df_european_decimal_with_none")],
)
def test_parse_european_decimal_columns_with_none(df):
    result = parse_european_decimal_columns(df, {"price": pl.Float32()})
    assert result["price"].to_list() == pytest.approx([1.23, None], rel=1e-6)


@pytest.mark.parametrize(
    argnames="df",
    argvalues=[lazy_fixture("df_european_decimal_simple")],
)
def test_parse_european_decimal_columns_wrong_column(df):
    with pytest.raises(
        ValueError, match="Expected column 'Wrong column' not found in dataframe"
    ):
        parse_european_decimal_columns(df, {"Wrong column": pl.Float32()})


@pytest.mark.parametrize(
    argnames="df",
    argvalues=[lazy_fixture("df_european_decimal_wrong_value")],
)
def test_parse_european_decimal_columns_wrong_value(df):
    with pytest.raises(
        Exception, match="Failed to parse one or more European decimal columns"
    ):
        parse_european_decimal_columns(df, {"price": pl.Float32()})
