import pytest
import polars as pl
from pytest_lazy_fixtures import lf as lazy_fixture
from {{ cookiecutter.project_slug }}.utils.commons import (
    add_timestamp_column,
    validate_columns,
)

"""
###
Tests for the function `add_timestamp_column`
###
"""


@pytest.mark.parametrize(
    argnames="df",
    argvalues=[lazy_fixture("df_add_timestamp_column_default")],
)
def test_add_timestamp_column_default(df: pl.DataFrame):
    result = add_timestamp_column(df)
    assert "ingestion_timestamp" in result.columns  # Check column exists
    assert result["ingestion_timestamp"].dtype == pl.Datetime  # Ensure correct dtype
    assert df.height == result.height  # Ensure row count is preserved
    assert (
        df["A"].to_list() == result["A"].to_list()
    )  # Ensure other columns are unchanged
    assert (
        len(set(result["ingestion_timestamp"].to_list())) == 1
    )  # All timestamps are the same


@pytest.mark.parametrize(
    argnames="df",
    argvalues=[lazy_fixture("df_add_timestamp_column_default")],
)
def test_add_timestamp_column_custom_name(df: pl.DataFrame):
    result = add_timestamp_column(df, column_name="ts")
    assert "ts" in result.columns  # Check column exists
    assert result["ts"].dtype == pl.Datetime  # Ensure correct dtype
    assert df.height == result.height  # Ensure row count is preserved
    assert (
        df["A"].to_list() == result["A"].to_list()
    )  # Ensure other columns are unchanged
    assert len(set(result["ts"].to_list())) == 1  # All timestamps are the same


@pytest.mark.parametrize(
    argnames="df",
    argvalues=[lazy_fixture("df_add_timestamp_column_empty")],
)
def test_add_timestamp_column_empty_dataframe(df: pl.DataFrame):
    result = add_timestamp_column(df)
    assert "ingestion_timestamp" in result.columns  # Check column exists
    assert result["ingestion_timestamp"].dtype == pl.Datetime  # Ensure correct dtype
    assert result.height == 0  # Ensure row count is zero


@pytest.mark.parametrize(
    argnames="df",
    argvalues=[
        lazy_fixture("df_add_timestamp_column_none"),
        lazy_fixture("df_add_timestamp_column_str"),
    ],
)
def test_add_timestamp_column_no_dataframe(df: pl.DataFrame):
    with pytest.raises(AttributeError):
        add_timestamp_column(df)


"""
###
Tests for the function `validate_columns`
###
"""

@pytest.mark.parametrize(
    argnames="df, schema",
    argvalues=[(lazy_fixture("df_validate_columns_expected_columns"), lazy_fixture("expected_schema_validate_columns"))],
)
def test_validate_columns(df, schema):
    validate_columns(df, schema)


@pytest.mark.parametrize(
    argnames="df, schema",
    argvalues=[
        (lazy_fixture("df_validate_columns_missing_columns"), lazy_fixture("expected_schema_validate_columns")),
        (lazy_fixture("df_validate_columns_extra_columns"), lazy_fixture("expected_schema_validate_columns")),
    ],
)
def test_validate_columns_missing_or_extra(df, schema):
    with pytest.raises(ValueError):
        validate_columns(df, schema)
