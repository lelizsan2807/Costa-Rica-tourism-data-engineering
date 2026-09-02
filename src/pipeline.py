from extract import (
    load_source_data,
    extract_periods,
    extract_table
)

from transform import clean_table

from validate import (
    validate_periods,
    validate_table,
    validate_demographics
)

from load import (
    save_csv,
    load_sqlite,
    check_database
)

from config import TABLE_DEFINITIONS


def main():

    # 1. Extract
    source_df = load_source_data()

    periods = extract_periods(source_df)
    validate_periods(periods)

    # 2. Transform
    tables = {}

    for table_name, definition in TABLE_DEFINITIONS.items():

        table = extract_table(
            source_df,
            periods,
            table_name,
            definition
        )

        table = clean_table(
            table,
            table_name
        )

        # 3. Validate
        validate_table(
            table,
            table_name,
            periods
        )

        tables[table_name] = table

        # 4. Save
        save_csv(table, table_name)

    # 5. Business validation
    validate_demographics(
        tables["fact_demographics"]
    )

    # 6. Load database
    load_sqlite(tables, periods)

    # 7. Verify
    check_database()


if __name__ == "__main__":
    main()