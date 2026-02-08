import pytest
import polars as pl


"""
Fixtures for the `add_timestamp_column` function.
"""


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


"""
Fixtures for the `validate_columns` function.
"""


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


"""
Fixtures for the `parse_european_decimal_columns` function.
"""


@pytest.fixture
def df_european_decimal_simple():
    df = pl.DataFrame({"price": ["1,23", "4,56"]})
    return df


@pytest.fixture
def df_european_decimal_multi():
    df = pl.DataFrame({"price": ["1,23"], "tax": ["0,20"]})
    return df


@pytest.fixture
def df_european_decimal_with_none():
    df = pl.DataFrame({"price": ["1,23", None]})
    return df


@pytest.fixture
def df_european_decimal_wrong_value():
    df = pl.DataFrame({"price": ["abc"]})
    return df


"""
Fixtures for the `cast_to_schema` function.
"""

@pytest.fixture()
def expected_schema_cast_to_schema():
    return pl.Schema(
        {
            "id": pl.Int16(),
            "datetime": pl.Datetime(time_unit="us"),
            "name": pl.String(),
            "value": pl.Float32(),
        }
    )


@pytest.fixture
def df_cast_to_schema_expected_columns():
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
def df_cast_to_schema_expected_columns_other_date_format():
    df = pl.DataFrame(
        {
            "id": [1, 2],
            "datetime": ["2023-01-01", "2023-02-01"],
            "name": ["A", "B"],
            "value": [10.0, 20.0],
        }
    )
    return df


"""
Fixtures for the `incremental_load` function.
"""


@pytest.fixture
def df_incremental_load_initial():
    df = pl.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "value": [10.0, 20.0, 30.0],
        }
    )
    return df


@pytest.fixture
def df_incremental_load_new_rows():
    df = pl.DataFrame(
        {
            "id": [4, 5],
            "name": ["David", "Eve"],
            "value": [40.0, 50.0],
        }
    )
    return df


@pytest.fixture
def df_incremental_load_update_rows():
    df = pl.DataFrame(
        {
            "id": [1, 2],
            "name": ["Alice Updated", "Bob Updated"],
            "value": [100.0, 200.0],
        }
    )
    return df


@pytest.fixture
def df_incremental_load_mixed():
    df = pl.DataFrame(
        {
            "id": [2, 4],
            "name": ["Bob Updated", "David"],
            "value": [200.0, 40.0],
        }
    )
    return df
