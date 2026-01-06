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


###
### Add Timestamp Column Tests
###


@pytest.fixture()
def expected_schema_validate_columns():
    return pl.Schema(
        {
            "id": pl.Int16(),
            "datetime": pl.Datetime(time_unit="us"),
            "name": pl.String(),
            "value": pl.Float32(),
        }
    )


@pytest.fixture
def df_validate_columns_expected_columns():
    df = pl.DataFrame(
        {
            "id": [1, 2],
            "datetime": ["01/01/2023", "01/02/2023"],
            "name": ["A", "B"],
            "value": [10.0, 20.0],
        }
    )
    return df


@pytest.fixture
def df_validate_columns_missing_columns():
    df = pl.DataFrame({"id": [1, 2], "name": ["A", "B"]})
    return df


@pytest.fixture
def df_validate_columns_extra_columns():
    df = pl.DataFrame(
        {
            "id": [1, 2],
            "datetime": ["01/01/2023", "01/02/2023"],
            "name": ["A", "B"],
            "value": [10.0, 20.0],
            "extra": [True, False],
            "another_extra": [3.14, 2.71],
        }
    )
    return df
