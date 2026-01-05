import pytest
import polars as pl


###
### Add Timestamp Column Tests
###


@pytest.fixture
def df_add_timestamp_column_default():
    df = pl.DataFrame(
        {
            "A": [1, 2, 3],
        }
    )
    return df


@pytest.fixture
def df_add_timestamp_column_empty():
    df = pl.DataFrame(
        {
            "A": [],
        }
    )
    return df


@pytest.fixture
def df_add_timestamp_column_none():
    return None


@pytest.fixture
def df_add_timestamp_column_str():
    return "Not a DataFrame"