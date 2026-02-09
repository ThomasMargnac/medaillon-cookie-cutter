import polars as pl
from deltalake import DeltaTable, write_deltalake


def full_load(
    df: pl.DataFrame,
    table_uri: str,
    storage_options: dict[str, str] | None = None,
) -> None:
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
