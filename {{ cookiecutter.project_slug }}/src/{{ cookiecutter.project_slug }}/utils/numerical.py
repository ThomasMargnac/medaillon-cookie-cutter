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
        If a specified column is not found in the DataFrame,
        or if parsing/casting fails for any column.
    """
    missing = set(columns) - set(df.columns)
    if missing:
        raise ValueError(f"Columns not found in dataframe: {sorted(missing)}")

    expressions = [
        pl.col(col).str.replace(",", ".").cast(dtype)
        for col, dtype in columns.items()
    ]

    try:
        return df.with_columns(expressions)
    except Exception as exc:
        raise ValueError("Failed to parse one or more European decimal columns") from exc
