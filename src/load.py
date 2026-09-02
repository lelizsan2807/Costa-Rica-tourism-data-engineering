from pandas import pd
from config import OUTPUT_DIR, DATABASE_FILE
from logging import logger
import sqlite3

def save_csv(
    df: pd.DataFrame,
    table_name: str) -> None:

    output_file = (
        OUTPUT_DIR /
        f"{table_name}.csv"
    )

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8"
    )

    logger.info(
        "Saved %s",
        output_file
    )

def load_sqlite(
    tables: dict,
    dim_period: pd.DataFrame
) -> None:

    logger.info(
        "Loading normalized data into SQLite"
    )

    with sqlite3.connect(DATABASE_FILE) as conn:

        # ----------------------------------------------------
        # Period dimension
        # ----------------------------------------------------

        dim_period.to_sql(
            "dim_period",
            conn,
            if_exists="replace",
            index=False
        )

        # ----------------------------------------------------
        # Fact tables
        # ----------------------------------------------------

        for table_name, df in tables.items():

            fact_df = df.copy()

            # Keep period_id as the foreign key.
            fact_df = fact_df.merge(
                dim_period[
                    ["period_id", "period"]
                ],
                on="period",
                how="left"
            )

            fact_df = fact_df[
                [
                    "period_id",
                    "period",
                    "year",
                    "quarter",
                    "dimension",
                    "category",
                    "value"
                ]
            ]

            fact_df.to_sql(
                table_name,
                conn,
                if_exists="replace",
                index=False
            )

            logger.info(
                "Loaded %d rows into %s",
                len(fact_df),
                table_name
            )

        # ----------------------------------------------------
        # Useful indexes
        # ----------------------------------------------------

        for table_name in tables:

            conn.execute(
                f"""
                CREATE INDEX IF NOT EXISTS
                idx_{table_name}_period
                ON {table_name}(period_id)
                """
            )

            conn.execute(
                f"""
                CREATE INDEX IF NOT EXISTS
                idx_{table_name}_category
                ON {table_name}(category)
                """
            )

        conn.commit()

    logger.info(
        "SQLite database created at %s",
        DATABASE_FILE
    )

def check_database() -> None:

    logger.info("Running database checks")

    with sqlite3.connect(DATABASE_FILE) as conn:

        tables = pd.read_sql_query(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """,
            conn
        )

        logger.info(
            "Database tables:\n%s",
            tables.to_string(index=False)
        )

        for table_name in [
            "fact_demographics",
            "fact_employment_structure",
            "fact_work_conditions",
            "fact_income"
        ]:

            result = pd.read_sql_query(
                f"""
                SELECT
                    COUNT(*) AS record_count,
                    COUNT(DISTINCT period) AS periods
                FROM {table_name}
                """,
                conn
            )

            logger.info(
                "%s:\n%s",
                table_name,
                result.to_string(index=False)
            )
