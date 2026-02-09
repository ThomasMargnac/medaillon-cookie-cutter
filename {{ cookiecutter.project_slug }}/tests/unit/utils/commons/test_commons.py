import pytest
import polars as pl
from pytest_lazy_fixtures import lf as lazy_fixture
from {{ cookiecutter.project_slug }}.utils.commons import (
    add_timestamp_column,
    validate_columns,
    parse_european_decimal_columns,
    cast_to_schema,
    full_load,
    incremental_load,
)


"""
Tests for the `add_timestamp_column` function.

These tests ensure that:
- the expected column is present
- the name of the new column is the one provided
- the data type of the new column is correct
- the timestamp values are consistent across all rows
- other columns remain unchanged
- wrong input types raise appropriate errors
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
Tests for the `validate_columns` function.

These tests ensure that:
- the happy path passes without errors
- inputs with missing or extra columns raises appropriate errors
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


"""
Tests for the `cast_to_schema` function.

These tests ensure that:
- 
"""


@pytest.mark.parametrize(
    argnames="df, schema",
    argvalues=[(lazy_fixture("df_cast_to_schema_expected_columns"), lazy_fixture("expected_schema_cast_to_schema"))],
)
def test_cast_to_schema(df, schema):
    casted_df = cast_to_schema(df, schema)
    assert casted_df.schema == schema


@pytest.mark.parametrize(
    argnames="df, schema",
    argvalues=[
        (
            lazy_fixture("df_cast_to_schema_expected_columns_other_date_format"),
            lazy_fixture("expected_schema_cast_to_schema"),
        )
    ],
)
def test_cast_to_schema_other_date_format(df, schema):
    casted_df = cast_to_schema(df, schema, datetime_format="%Y-%m-%d")
    assert casted_df.schema == schema


@pytest.mark.parametrize(
    argnames="df, schema",
    argvalues=[
        (
            lazy_fixture("df_cast_to_schema_expected_columns_other_date_format"),
            lazy_fixture("expected_schema_cast_to_schema"),
        )
    ],
)
def test_cast_to_schema_wrong_date_format(df, schema):
    with pytest.raises(ValueError):
        cast_to_schema(df, schema)


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
