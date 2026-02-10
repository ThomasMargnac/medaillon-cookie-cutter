import polars as pl
from deltalake import DeltaTable, write_deltalake


def full_load(
    df: pl.DataFrame,
    table_uri: str,
    storage_options: dict[str, str] | None = None,
) -> None:
    """
    Perform a full load (overwrite) of a DataFrame into a Delta table.

    This function writes the entire DataFrame to a Delta table, replacing any
    existing data in the table.

    Parameters
    ----------
    df : pl.DataFrame
        The Polars DataFrame to write to the Delta table.
    table_uri : str
        The URI path to the Delta table (local path or cloud storage path).
    storage_options : dict[str, str] | None, optional
        Storage configuration options for cloud storage access (e.g., AWS credentials).
        Default is None.

    Returns
    -------
    None
    """
    write_deltalake(
        table_or_uri=table_uri,
        data=df.to_arrow(),
        mode="overwrite",
        storage_options=storage_options,
    )


def incremental_load(
    df: pl.DataFrame,
    table_uri: str,
    predicate: str,
    storage_options: dict[str, str] | None = None,
) -> None:
    """
    Perform an incremental load (upsert) of a DataFrame into a Delta table.

    This function merges the DataFrame with an existing Delta table using the
    specified predicate. If the table doesn't exist, it creates a new one.
    Matching records are updated, and new records are inserted.

    Parameters
    ----------
    df : pl.DataFrame
        The Polars DataFrame containing new or updated data to merge.
    table_uri : str
        The URI path to the Delta table (local path or cloud storage path).
    predicate : str
        The merge predicate used to match records between source and target
        (e.g., "source.id = target.id").
    storage_options : dict[str, str] | None, optional
        Storage configuration options for cloud storage access (e.g., AWS credentials).
        Default is None.

    Returns
    -------
    None
    """
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
