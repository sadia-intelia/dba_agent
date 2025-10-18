# tools.py
import sqlite3
from typing import Dict, Any


def run_sql_query(query: str) -> Dict:
    """Runs a SELECT query against a SQLite database."""
    try:
        # 🚫 Only allow SELECT queries
        if not query.strip().lower().startswith("select"):
            return {"status": "error", "message": "Only SELECT queries are allowed."}

        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute(query)

        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()

        return {
            "status": "success",
            "columns": columns,
            "rows": rows
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


def check_or_create_employees_index() -> Dict[str, Any]:
    """
    Checks if the 'employees' table has any indexes.
    If none exist, creates an index on the 'name' column.
    """
    #TODO extention of any table has been added in last 6 hours
    table_name = "employees"
    index_name = "idx_employees_name"

    try:
        conn = sqlite3.connect('./mydatabase.db')
        cursor = conn.cursor()
        print("inside tool")
        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            return {"status": "error", "message": f"Table '{table_name}' does not exist."}

        # Check for existing indexes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name=?", (table_name,))
        existing_indexes = cursor.fetchall()

        if existing_indexes:
            return {
                "status": "success",
                "message": f"Table '{table_name}' already has indexes.",
                "indexes": [i[0] for i in existing_indexes]
            }

        # If no indexes found, create one on 'name'
        cursor.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}(name);")
        conn.commit()

        return {
            "status": "success",
            "message": f"No indexes found. Created index '{index_name}' on column 'name'."
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
# ✅ ADK-compatible wrapper
# check_or_create_index_tool = Tool.from_function(
#     check_or_create_employees_index,
#     name="check_or_create_employees_index",
#     description="Checks for indexes on the 'employees' table "
# )