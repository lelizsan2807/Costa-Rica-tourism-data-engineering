import pandas as pd
import logging as logger

def clean_table(
    df: pd.DataFrame,
    table_name: str
) -> pd.DataFrame:
    """
    Clean and standardize extracted observations.

    Rules:
    - Remove unnecessary whitespace from text columns.
    - Convert Excel "-" values to missing values.
    - Convert observations to numeric values.
    - Keep rows with missing values.
    - Reject negative values.
    - Store numeric observations as float.
    """

    logger.info("Cleaning %s", table_name)

    # Work on a copy so the original DataFrame is not modified.
    df = df.copy()

    df["period"] = (
        df["period"]
        .astype(str)
        .str.strip()
    )

    df["dimension"] = (
        df["dimension"]
        .astype(str)
        .str.strip()
    )

    df["category"] = (
        df["category"]
        .astype(str)
        .str.strip()
    )

    df["value"] = df["value"].replace("-", pd.NA)

    df["value"] = pd.to_numeric(
        df["value"],
        errors="coerce"
    )

    missing_count = df["value"].isna().sum()

    if missing_count > 0:
        logger.warning(
            "%s: found %d missing observations",
            table_name,
            missing_count
        )

    negative_count = (
        df["value"]
        .dropna()
        .lt(0)
        .sum()
    )

    if negative_count > 0:
        raise ValueError(
            f"{table_name}: found "
            f"{negative_count} negative values."
        )

    df["value"] = df["value"].astype(float)

    logger.info(
        "%s: cleaned %d observations",
        table_name,
        len(df)
    )

    return df



def create_period_dimension(periods: pd.DataFrame) -> pd.DataFrame:
    """
    Create a reusable period dimension.
    """

    dim_period = periods[
        ["year", "quarter", "period"]
    ].copy()

    dim_period["period_id"] = range(
        1,
        len(dim_period) + 1
    )

    dim_period = dim_period[
        [
            "period_id",
            "year",
            "quarter",
            "period"
        ]
    ]

    return dim_period