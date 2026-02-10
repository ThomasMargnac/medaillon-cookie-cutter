import polars as pl
from datetime import datetime


def validate_columns(
    df: pl.DataFrame,
    expected_schema: pl.Schema,
    skip_full_null_check: set[str] | None = None,
) -> None:
    """
    Validate that a DataFrame contains the expected columns and non-null data.

    This function checks that the DataFrame has exactly the columns specified in
    the expected schema (no missing, no extra) and verifies that required columns
    are not entirely null.

    Parameters
    ----------
    df : pl.DataFrame
        The Polars DataFrame to validate.
    expected_schema : pl.Schema
        The expected schema defining the required column names.
    skip_full_null_check : set[str] | None, optional
        A set of column names to skip when checking for all-null columns.
        Default is None (empty set).

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If there are missing or extra columns compared to the expected schema,
        or if required columns contain only null values.
    """
    skip_full_null_check = skip_full_null_check or set()

    expected = set(expected_schema.keys())
    actual = set(df.columns)

    missing = expected - actual
    extra = actual - expected

    if missing or extra:
        raise ValueError(
            f"Schema mismatch: missing={sorted(missing)}, extra={sorted(extra)}"
        )

    columns_to_check = sorted(expected - skip_full_null_check)

    if not columns_to_check:
        return

    null_counts = df.select(columns_to_check).null_count()
    full_null_columns = [
        col
        for col, count in zip(columns_to_check, null_counts.row(0))
        if count == df.height
    ]

    if full_null_columns:
        raise ValueError(
            "Columns are empty (all values are null) but are required: "
            f"{full_null_columns}"
        )


def cast_to_schema(
    df: pl.DataFrame, schema: pl.Schema, datetime_format: str = "%d/%m/%Y"
) -> pl.DataFrame:
    """
    Cast DataFrame columns to match a target schema.

    This function converts each column in the DataFrame to the data type specified
    in the schema. For datetime columns stored as strings, it parses them using
    the provided format string.

    Parameters
    ----------
    df : pl.DataFrame
        The input Polars DataFrame to cast.
    schema : pl.Schema
        The target schema defining column names and their target data types.
    datetime_format : str, optional
        The format string for parsing datetime columns from strings.
        Default is "%d/%m/%Y" (day/month/year).

    Returns
    -------
    pl.DataFrame
        A new DataFrame with all columns cast to the target schema types.

    Raises
    ------
    ValueError
        If casting fails for any column.
    """
    source_schema = df.schema

    expressions = [
        pl.col(col).str.strptime(pl.Datetime, format=datetime_format, strict=True)
        if isinstance(target_dtype, pl.Datetime) and source_schema[col] == pl.String
        else pl.col(col).cast(target_dtype)
        for col, target_dtype in schema.items()
    ]

    try:
        return df.select(expressions)
    except Exception as exc:
        raise ValueError("Failed to cast dataframe to expected schema.") from exc


def add_timestamp_column(
    df: pl.DataFrame, column_name: str = "ingestion_timestamp"
) -> pl.DataFrame:
    """
    Add a timestamp column to a DataFrame with the current datetime.

    This function appends a new column containing the current timestamp to the
    DataFrame, typically used to track when data was ingested or processed.

    Parameters
    ----------
    df : pl.DataFrame
        The input Polars DataFrame.
    column_name : str, optional
        The name for the new timestamp column.
        Default is "ingestion_timestamp".

    Returns
    -------
    pl.DataFrame
        A new DataFrame with the timestamp column added.
    """
    return df.with_columns(pl.lit(datetime.now()).alias(column_name))
