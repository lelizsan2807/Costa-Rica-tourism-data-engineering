import pandas as pd
import logging as logger

def validate_periods(
    periods: pd.DataFrame
) -> None:
    """
    Validate the expected 2010 Q3 -> 2026 Q1 period range.
    """

    logger.info("Validating period dimension")

    expected_periods = pd.period_range(
        start="2010Q3",
        end="2026Q1",
        freq="Q"
    )

    expected = [
        f"{p.year}-Q{p.quarter}"
        for p in expected_periods
    ]

    actual = periods["period"].tolist()

    if actual != expected:
        raise ValueError(
            "Period validation failed.\n"
            f"Expected {len(expected)} periods from "
            f"{expected[0]} to {expected[-1]}.\n"
            f"Found {len(actual)} periods from "
            f"{actual[0]} to {actual[-1]}."
        )

    logger.info(
        "Period validation passed: %d quarters",
        len(actual)
    )


def validate_table(
    df: pd.DataFrame,
    table_name: str,
    periods: pd.DataFrame
) -> None:
    """
    General data-quality checks.
    """

    logger.info("Validating %s", table_name)

    # --------------------------------------------------------
    # Required columns
    # --------------------------------------------------------

    required_columns = {
        "period",
        "year",
        "quarter",
        "dimension",
        "category",
        "value"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"{table_name}: missing columns "
            f"{missing_columns}"
        )

    # --------------------------------------------------------
    # No missing values in key fields
    # --------------------------------------------------------

    key_columns = [
        "period",
        "year",
        "quarter",
        "dimension",
        "category"
    ]

    for column in key_columns:

        missing = df[column].isna().sum()

        if missing > 0:
            raise ValueError(
                f"{table_name}: {missing} missing values "
                f"in '{column}'."
            )

    # --------------------------------------------------------
    # No duplicate observations
    # --------------------------------------------------------

    duplicates = df.duplicated(
        subset=[
            "period",
            "dimension",
            "category"
        ]
    ).sum()

    if duplicates > 0:
        raise ValueError(
            f"{table_name}: found {duplicates} duplicate "
            "observations."
        )

    # --------------------------------------------------------
    # Period coverage
    # --------------------------------------------------------

    expected_periods = set(
        periods["period"]
    )

    actual_periods = set(
        df["period"]
    )

    missing_periods = expected_periods - actual_periods

    if missing_periods:
        raise ValueError(
            f"{table_name}: missing periods: "
            f"{sorted(missing_periods)}"
        )

    # --------------------------------------------------------
    # No negative values
    # --------------------------------------------------------

    negative_values = (
        df["value"] < 0
    ).sum()

    if negative_values > 0:
        raise ValueError(
            f"{table_name}: found negative values."
        )

    logger.info(
        "%s validation passed: %d records",
        table_name,
        len(df)
    )

def validate_demographics(
    df: pd.DataFrame
) -> None:
    """
    Validate the relationship:

        Total = Hombre + Mujer

    for every period.
    """

    logger.info(
        "Running demographic reconciliation checks"
    )

    sex = df[
        df["dimension"] == "sex"
    ].pivot(
        index="period",
        columns="category",
        values="value"
    )

    totals = df[
        df["dimension"] == "overall"
    ].set_index("period")["value"]

    for period in sex.index:

        if "Hombre" not in sex.columns:
            continue

        if "Mujer" not in sex.columns:
            continue

        if period not in totals.index:
            continue

        male = sex.loc[period, "Hombre"]
        female = sex.loc[period, "Mujer"]
        total = totals.loc[period]

        calculated_total = male + female

        if abs(calculated_total - total) > 0.01:

            raise ValueError(
                f"Demographic reconciliation failed "
                f"for {period}: "
                f"Hombre ({male}) + Mujer ({female}) "
                f"!= Total ({total})"
            )

    logger.info(
        "Demographic reconciliation passed"
    )
