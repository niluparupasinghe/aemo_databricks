"""
00_setup_unity_catalog.py
=========================
Databricks Free Edition / Serverless Setup Script

Purpose:
- Creates the `bronze` schema inside the default `workspace` catalog (Unity Catalog).
- Creates the `landing` Managed Volume (`/Volumes/workspace/bronze/landing`) for storing raw 5-minute AEMO ZIP files.
- Creates the `workspace.bronze.meta_file_control_log` Delta table for exact-once state tracking.
"""

from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

CATALOG = "aemo"
SCHEMA = "bronze"
VOLUME_NAME = "landing"


def main():
    print(f"[Setup] Initializing Unity Catalog objects in `{CATALOG}.{SCHEMA}`...")

    # 1. Create Schema
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")
    print(f"  -> Schema `{CATALOG}.{SCHEMA}` verified.")

    # 2. Create Managed Volume for raw Landing ZIP files
    spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.{SCHEMA}.{VOLUME_NAME}")
    volume_path = f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME_NAME}"
    print(f"  -> Managed Volume `{volume_path}` verified.")

    # 3. Create Control Log Delta Table if it does not exist
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {CATALOG}.{SCHEMA}.meta_file_control_log (
            file_name STRING,
            feed_name STRING,
            landing_date_folder STRING,
            landing_path STRING,
            file_size_bytes BIGINT,
            status STRING,
            downloaded_at_utc STRING,
            ingested_at_utc STRING,
            purged_at_utc STRING,
            bronze_row_count BIGINT
        )
        USING DELTA
    """)
    print(f"  -> Delta Table `{CATALOG}.{SCHEMA}.meta_file_control_log` verified.")


if __name__ == "__main__":
    main()
