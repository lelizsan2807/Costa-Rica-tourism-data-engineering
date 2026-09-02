import pandas as pd
from logging import logger



def clean_table(
    df: pd.DataFrame,
    table_name: str
) -> pd.DataFrame:
    """
    Clean and standardize extracted observations.
    """

    logger.info("Cleaning %s", table_name)

    df = df.copy()

    # Standardize strings.
    df["period"] = df["period"].astype(str).str.strip()
    df["dimension"] = df["dimension"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()

    # Convert observations to numeric.
    df["value"] = pd.to_numeric(
        df["value"],
        errors="coerce"
    )

    # Remove observations that cannot be interpreted as numbers.
    invalid_count = df["value"].isna().sum()

    if invalid_count > 0:
        logger.warning(
            "%s: removing %d non-numeric observations",
            table_name,
            invalid_count
        )

        df = df.dropna(subset=["value"])

    # Check negative values.
    negative_count = (df["value"] < 0).sum()

    if negative_count > 0:
        raise ValueError(
            f"{table_name}: found {negative_count} negative values."
        )

    # Preserve decimals where they exist.
    df["value"] = df["value"].astype(float)

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