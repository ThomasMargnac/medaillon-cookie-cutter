import polars as pl


def parse_european_decimal_columns(
    df: pl.DataFrame,
    columns: dict[str, pl.DataType],
) -> pl.DataFrame:
    """
    Parse European-format decimal columns by replacing commas with periods.

    This function converts decimal columns that use European formatting (comma as
    decimal separator) to standard format (period as decimal separator) and casts
    them to the specified data types.

    Parameters
    ----------
    df : pl.DataFrame
        The input Polars DataFrame containing columns to parse.
    columns : dict[str, pl.DataType]
        A dictionary mapping column names to their target Polars data types.
        Each column will have commas replaced with periods before casting.

    Returns
    -------
    pl.DataFrame
        A new DataFrame with the specified columns parsed and cast to the target types.

    Raises
    ------
    ValueError
        If a specified column is not found in the DataFrame.
    Exception
        If parsing or casting fails for any column.
    """
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
