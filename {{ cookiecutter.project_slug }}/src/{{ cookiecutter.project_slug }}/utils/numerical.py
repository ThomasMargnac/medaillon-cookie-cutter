import polars as pl


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
