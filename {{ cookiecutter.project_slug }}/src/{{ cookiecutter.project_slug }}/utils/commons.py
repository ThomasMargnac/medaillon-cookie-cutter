import polars as pl
from datetime import datetime
from deltalake import DeltaTable, write_deltalake


def validate_columns(
    df: pl.DataFrame,
    expected_schema: pl.Schema,
    skip_full_null_check: set[str] | None = None,
) -> None:
    skip_full_null_check = skip_full_null_check or set()

    expected = set(expected_schema.keys())
    actual = set(df.columns)

    missing = expected - actual
    extra = actual - expected

    if missing or extra:
        raise ValueError(
            f"Schema mismatch: missing={sorted(missing)}, extra={sorted(extra)}"
        )

    columns_to_check = expected - skip_full_null_check

    full_null_columns = [
        col for col in columns_to_check if df[col].null_count() == df.height
    ]

    if full_null_columns:
        raise ValueError(
            "Columns are empty (all values are null) but are required: "
            f"{sorted(full_null_columns)}"
        )


def cast_to_schema(
    df: pl.DataFrame, schema: pl.Schema, datetime_format: str = "%d/%m/%Y"
) -> pl.DataFrame:
    expressions = []

    for column, dtype in schema.items():
        if isinstance(dtype, pl.Datetime) and df[column].dtype == pl.String:
            expr = (
                pl.col(column)
                .str.strptime(pl.Datetime, format=datetime_format, strict=True)
                .alias(column)
            )

        else:
            expr = pl.col(column).cast(dtype).alias(column)

        expressions.append(expr)

    try:
        return df.select(expressions)
    except Exception as exc:
        raise ValueError("Failed to cast dataframe to expected schema.") from exc


def parse_european_decimal_columns(
    df: pl.DataFrame,
    columns: dict[str, pl.DataType],
) -> pl.DataFrame:
    expressions = []

    for column, dtype in columns.items():
        if column not in df.columns:
            raise ValueError(f"Expected column '{column}' not found in dataframe")

        expressions.append(
            pl.when(pl.col(column).is_null())
            .then(None)
            .otherwise(pl.col(column).str.replace(",", ".").cast(dtype))
            .alias(column)
        )

    try:
        return df.with_columns(expressions)
    except Exception as exc:
        raise Exception("Failed to parse one or more European decimal columns") from exc


def add_timestamp_column(
    df: pl.DataFrame, column_name: str = "ingestion_timestamp"
) -> pl.DataFrame:
    return df.with_columns(pl.lit(datetime.now()).alias(column_name))


def incremental_load(
    df: pl.DataFrame,
    table_uri: str,
    predicate: str,
    storage_options: dict[str, str] | None = None,
) -> None:
    if DeltaTable.is_deltatable(table_uri, storage_options=storage_options):
        dt = DeltaTable(table_uri, storage_options=storage_options)
        (
            dt.merge(
                source=df.to_arrow(),
                predicate=predicate,
                source_alias="source",
                target_alias="target",
            )
            .when_matched_update_all()
            .when_not_matched_insert_all()
            .execute()
        )
    else:
        write_deltalake(
            table_or_uri=table_uri,
            data=df.to_arrow(),
            storage_options=storage_options,
        )
