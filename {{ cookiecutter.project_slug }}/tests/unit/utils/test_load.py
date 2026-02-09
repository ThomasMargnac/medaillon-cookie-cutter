import pytest
import polars as pl
from pytest_lazy_fixtures import lf as lazy_fixture
from {{ cookiecutter.project_slug }}.utils.load import (
    full_load,
    incremental_load,
)


"""
Tests for the `full_load` function.

These tests ensure that:
- a new Delta table is created when it does not exist
- existing data is fully replaced on subsequent loads
- wrong input types raise appropriate errors
"""


@pytest.mark.parametrize(
    argnames="df",
    argvalues=[lazy_fixture("df_full_load")],
)
def test_full_load_first_load(df, tmp_path):
    table_uri = str(tmp_path / "test_table")
    full_load(df, table_uri)
    result = pl.read_delta(table_uri)
    assert result.height == 3
    assert sorted(result["id"].to_list()) == [1, 2, 3]
    assert sorted(result["name"].to_list()) == ["Alice", "Bob", "Charlie"]


@pytest.mark.parametrize(
    argnames="initial_df, overwrite_df",
    argvalues=[
        (
            lazy_fixture("df_full_load"),
            lazy_fixture("df_full_load_overwrite"),
        )
    ],
)
def test_full_load_overwrites_existing_data(initial_df, overwrite_df, tmp_path):
    table_uri = str(tmp_path / "test_table")
    full_load(initial_df, table_uri)
    full_load(overwrite_df, table_uri)
    result = pl.read_delta(table_uri)
    assert result.height == 2
    assert sorted(result["id"].to_list()) == [4, 5]
    assert sorted(result["name"].to_list()) == ["David", "Eve"]


@pytest.mark.parametrize(
    argnames="df",
    argvalues=[
        lazy_fixture("df_add_timestamp_column_none"),
        lazy_fixture("df_add_timestamp_column_str"),
    ],
)
def test_full_load_wrong_input_type(df, tmp_path):
    table_uri = str(tmp_path / "test_table")
    with pytest.raises(AttributeError):
        full_load(df, table_uri)


"""
Tests for the `incremental_load` function.

These tests ensure that:
- a new Delta table is created when it does not exist
- new rows are inserted when they do not match existing rows
- existing rows are updated when they match the predicate
- a mix of new and updated rows is handled correctly
- wrong input types raise appropriate errors
"""

PREDICATE = "source.id = target.id"


@pytest.mark.parametrize(
    argnames="df",
    argvalues=[lazy_fixture("df_incremental_load_initial")],
)
def test_incremental_load_first_load(df, tmp_path):
    table_uri = str(tmp_path / "test_table")
    incremental_load(df, table_uri, PREDICATE)
    result = pl.read_delta(table_uri)
    assert result.height == 3
    assert sorted(result["id"].to_list()) == [1, 2, 3]
    assert sorted(result["name"].to_list()) == ["Alice", "Bob", "Charlie"]


@pytest.mark.parametrize(
    argnames="initial_df, new_df",
    argvalues=[
        (
            lazy_fixture("df_incremental_load_initial"),
            lazy_fixture("df_incremental_load_new_rows"),
        )
    ],
)
def test_incremental_load_insert_new_rows(initial_df, new_df, tmp_path):
    table_uri = str(tmp_path / "test_table")
    incremental_load(initial_df, table_uri, PREDICATE)
    incremental_load(new_df, table_uri, PREDICATE)
    result = pl.read_delta(table_uri)
    assert result.height == 5
    assert sorted(result["id"].to_list()) == [1, 2, 3, 4, 5]


@pytest.mark.parametrize(
    argnames="initial_df, update_df",
    argvalues=[
        (
            lazy_fixture("df_incremental_load_initial"),
            lazy_fixture("df_incremental_load_update_rows"),
        )
    ],
)
def test_incremental_load_update_existing_rows(initial_df, update_df, tmp_path):
    table_uri = str(tmp_path / "test_table")
    incremental_load(initial_df, table_uri, PREDICATE)
    incremental_load(update_df, table_uri, PREDICATE)
    result = pl.read_delta(table_uri).sort("id")
    assert result.height == 3
    assert result["name"].to_list() == ["Alice Updated", "Bob Updated", "Charlie"]
    assert result["value"].to_list() == [100.0, 200.0, 30.0]


@pytest.mark.parametrize(
    argnames="initial_df, mixed_df",
    argvalues=[
        (
            lazy_fixture("df_incremental_load_initial"),
            lazy_fixture("df_incremental_load_mixed"),
        )
    ],
)
def test_incremental_load_mixed_upsert(initial_df, mixed_df, tmp_path):
    table_uri = str(tmp_path / "test_table")
    incremental_load(initial_df, table_uri, PREDICATE)
    incremental_load(mixed_df, table_uri, PREDICATE)
    result = pl.read_delta(table_uri).sort("id")
    assert result.height == 4
    assert result["id"].to_list() == [1, 2, 3, 4]
    assert result["name"].to_list() == ["Alice", "Bob Updated", "Charlie", "David"]


@pytest.mark.parametrize(
    argnames="df",
    argvalues=[
        lazy_fixture("df_add_timestamp_column_none"),
        lazy_fixture("df_add_timestamp_column_str"),
    ],
)
def test_incremental_load_wrong_input_type(df, tmp_path):
    table_uri = str(tmp_path / "test_table")
    with pytest.raises(AttributeError):
        incremental_load(df, table_uri, PREDICATE)
