import pandas as pd
from config import INPUT_FILE, SHEET_NAME
import logging as logger

def load_source_data() -> pd.DataFrame:

    """
    Load the semi-structured Excel worksheet without assuming
    that it has a conventional single header row.
    """

    logger.info("Loading Excel workbook: %s", INPUT_FILE)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    df = pd.read_excel(
        INPUT_FILE,
        sheet_name=SHEET_NAME,
        header=None
    )

    logger.info(
        "Loaded sheet '%s' with shape %s",
        SHEET_NAME,
        df.shape
    )

    return df

def extract_periods(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract year and quarter from the multi-level header.

    In this workbook:
        Excel row 5  -> years
        Excel row 6  -> quarters
        Excel columns 3 onward -> observations

    """

    logger.info("Extracting year and quarter information")

    records = []

    year_row = 4
    quarter_row = 5

    for col in range(2, df.shape[1]):

        year = df.iloc[year_row, col]
        quarter = df.iloc[quarter_row, col]

        if pd.isna(year):
            if records:
                year = records[-1]["year"]

        if pd.isna(year) or pd.isna(quarter):
            continue

        year = int(year)

        quarter = str(quarter).strip()

        quarter_map = {
            "I": 1,
            "II": 2,
            "III": 3,
            "IV": 4
        }

        if quarter not in quarter_map:
            logger.warning(
                "Unknown quarter '%s' in column %s",
                quarter,
                col
            )
            continue

        quarter_number = quarter_map[quarter]

        period = f"{year}-Q{quarter_number}"

        records.append({
            "column_index": col,
            "year": year,
            "quarter": quarter_number,
            "period": period
        })

    periods = pd.DataFrame(records)

    if periods.empty:
        raise ValueError("No periods were extracted from the workbook.")

    logger.info(
        "Extracted %d periods: %s → %s",
        len(periods),
        periods.iloc[0]["period"],
        periods.iloc[-1]["period"]
    )

    return periods

def extract_table(
    df: pd.DataFrame,
    periods: pd.DataFrame,
    table_name: str,
    definition: dict
) -> pd.DataFrame:
    """
    Extract one logical table from the semi-structured worksheet
    and convert it into long/normalized format.
    """

    logger.info("Extracting %s", table_name)

    records = []

    for row_number, (dimension, category) in definition["rows"].items():

        for _, period_info in periods.iterrows():

            column_index = period_info["column_index"]

            value = df.iloc[row_number, column_index]

            # Ignore completely empty cells.
            if pd.isna(value):
                continue

            records.append({
                "period": period_info["period"],
                "year": period_info["year"],
                "quarter": period_info["quarter"],
                "dimension": dimension,
                "category": category,
                "value": value
            })

    result = pd.DataFrame(records)

    if result.empty:
        raise ValueError(
            f"No records extracted for {table_name}"
        )

    return result